import { useState, useEffect } from "react";
import { ChevronRight, Folder, FileText, RefreshCw, ExternalLink } from "lucide-react";

interface TreeNode {
  name: string;
  type: "file" | "dir";
  children?: TreeNode[];
}

interface TreeData {
  root: string;
  children: TreeNode[];
}

const VIEWABLE = new Set([".html", ".png", ".jpg", ".jpeg", ".svg"]);

function getExt(name: string) {
  const dot = name.lastIndexOf(".");
  return dot >= 0 ? name.slice(dot).toLowerCase() : "";
}

function TreeItem({
  node,
  depth = 0,
  parentPath = "",
}: {
  node: TreeNode;
  depth?: number;
  parentPath?: string;
}) {
  const [open, setOpen] = useState(depth < 1);
  const isDir = node.type === "dir";
  const hasChildren = isDir && node.children && node.children.length > 0;
  const filePath = parentPath ? `${parentPath}/${node.name}` : node.name;
  const ext = getExt(node.name);
  const isViewable = !isDir && VIEWABLE.has(ext);

  const handleClick = () => {
    if (isDir) {
      setOpen(!open);
    } else if (isViewable) {
      const encodedPath = filePath.split("/").map(encodeURIComponent).join("/");
      window.open(`/api/file/${encodedPath}`, "_blank");
    }
  };

  return (
    <div>
      <button
        onClick={handleClick}
        className={`group flex items-center gap-1.5 w-full text-left py-0.5 hover:bg-white/[0.03] rounded px-1 transition-colors ${
          isDir || isViewable ? "cursor-pointer" : "cursor-default"
        }`}
        style={{ paddingLeft: `${depth * 16 + 4}px` }}
      >
        {isDir ? (
          <ChevronRight
            className={`w-3 h-3 text-slate-600 transition-transform shrink-0 ${
              open ? "rotate-90" : ""
            }`}
          />
        ) : (
          <span className="w-3 shrink-0" />
        )}
        {isDir ? (
          <Folder className="w-3.5 h-3.5 text-cyan-500/70 shrink-0" />
        ) : (
          <FileText
            className={`w-3.5 h-3.5 shrink-0 ${
              isViewable ? "text-cyan-500/50" : "text-slate-600"
            }`}
          />
        )}
        <span
          className={`text-xs truncate ${
            isDir
              ? "text-slate-300 font-medium"
              : isViewable
              ? "text-cyan-400/70 group-hover:text-cyan-300 transition-colors"
              : "text-slate-500"
          }`}
        >
          {node.name}
        </span>
        {isDir && node.children && (
          <span className="text-[9px] text-slate-700 ml-1">
            {node.children.length}
          </span>
        )}
        {isViewable && (
          <ExternalLink className="w-2.5 h-2.5 text-cyan-500/30 opacity-0 group-hover:opacity-100 transition-opacity ml-auto shrink-0" />
        )}
      </button>
      {isDir && open && hasChildren && (
        <div>
          {node.children!.map((child, i) => (
            <TreeItem
              key={child.name + i}
              node={child}
              depth={depth + 1}
              parentPath={filePath}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export function FileStructure() {
  const [tree, setTree] = useState<TreeData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchTree = () => {
    setLoading(true);
    setError(null);
    fetch("/api/tree")
      .then((res) => {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then((data) => {
        setTree(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(fetchTree, []);

  return (
    <div className="w-full max-w-2xl mx-auto px-6 py-6 overflow-y-auto max-h-[85vh] animate-fade-in">
      <div className="text-center mb-6">
        <div className="text-sm text-cyan-300/50 uppercase tracking-widest mb-2 font-mono">
          File Structure
        </div>
        <h1 className="text-2xl font-bold text-cyan-400 mb-1">/science</h1>
        <p className="text-[10px] text-slate-600 mt-1">
          Click any .html or image file to open it
        </p>
        <div className="flex justify-center mt-3">
          <button
            onClick={fetchTree}
            className="flex items-center gap-1.5 text-[10px] text-slate-500 hover:text-slate-300 transition-colors"
          >
            <RefreshCw className={`w-3 h-3 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-700/50 bg-slate-900/50 p-3 font-mono">
        {loading && !tree && (
          <div className="text-xs text-slate-500 text-center py-8">
            Loading...
          </div>
        )}
        {error && (
          <div className="text-xs text-red-400/70 text-center py-8">
            Failed to load: {error}
          </div>
        )}
        {tree &&
          tree.children.map((node, i) => (
            <TreeItem key={node.name + i} node={node} />
          ))}
      </div>
    </div>
  );
}
