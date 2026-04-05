const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const REPOS_DIR = "/data/repos";
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

function getRepoDir(repoFullName) {
  return path.join(REPOS_DIR, ...repoFullName.split("/"));
}

function gitExec(cmd, cwd) {
  return execSync(cmd, { cwd, timeout: 60000, shell: true }).toString().trim();
}

function ensureRepo(repoFullName) {
  const repoDir = getRepoDir(repoFullName);
  const repoUrl = `https://${GITHUB_TOKEN}@github.com/${repoFullName}.git`;

  if (!fs.existsSync(path.join(repoDir, ".git"))) {
    console.log(`[repos] Cloning ${repoFullName}...`);
    const parentDir = path.dirname(repoDir);
    fs.mkdirSync(parentDir, { recursive: true });
    execSync(`git clone "${repoUrl}" "${repoDir}"`, { timeout: 120000, shell: true });
    console.log(`[repos] Cloned ${repoFullName}`);
  } else {
    console.log(`[repos] Fetching ${repoFullName}...`);
    gitExec("git fetch origin", repoDir);
  }

  return repoDir;
}

function checkoutBranch(repoDir, branch) {
  gitExec(`git checkout ${branch}`, repoDir);
  gitExec(`git pull origin ${branch}`, repoDir);
  console.log(`[repos] On branch ${branch}, up to date`);
}

function commitAndPush(repoDir, message, branch) {
  gitExec("git add -A", repoDir);

  // Check if there are changes to commit
  try {
    execSync("git diff --cached --quiet", { cwd: repoDir, shell: true });
    console.log("[repos] No changes to commit");
    return null;
  } catch {
    // Non-zero exit = there are staged changes
  }

  const escapedMsg = message.replace(/"/g, '\\"');
  gitExec(`git commit -m "${escapedMsg}"`, repoDir);
  const sha = gitExec("git rev-parse --short HEAD", repoDir);

  // Pull with rebase before pushing to avoid conflicts
  try {
    gitExec(`git pull --rebase origin ${branch}`, repoDir);
  } catch (err) {
    console.error(`[repos] Rebase failed: ${err.message}`);
  }

  gitExec(`git push origin ${branch}`, repoDir);
  console.log(`[repos] Pushed ${sha} to ${branch}`);
  return sha;
}

function listRepos() {
  if (!fs.existsSync(REPOS_DIR)) return [];
  const repos = [];
  const owners = fs.readdirSync(REPOS_DIR).filter(f => {
    return fs.statSync(path.join(REPOS_DIR, f)).isDirectory();
  });
  for (const owner of owners) {
    const ownerDir = path.join(REPOS_DIR, owner);
    const names = fs.readdirSync(ownerDir).filter(f => {
      return fs.statSync(path.join(ownerDir, f)).isDirectory();
    });
    for (const name of names) {
      repos.push(`${owner}/${name}`);
    }
  }
  return repos;
}

module.exports = { getRepoDir, ensureRepo, checkoutBranch, commitAndPush, listRepos };
