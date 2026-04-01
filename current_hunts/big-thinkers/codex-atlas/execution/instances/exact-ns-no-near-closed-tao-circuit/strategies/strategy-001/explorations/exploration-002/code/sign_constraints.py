from itertools import product


def main():
    rows = []
    for c2, c3 in product((2, -2), repeat=2):
        # amplifier uses one role-2 mode and two role-3 modes with arbitrary sign choices
        # after the two a1^2 channels force k2 = c2*k1 and k3 = c3*k1.
        sols = []
        for alpha, beta, gamma in product((1, -1), repeat=3):
            total = alpha * c3 + beta * c2 + gamma * c3
            if total == 0:
                sols.append((alpha, beta, gamma))
        rows.append((c2, c3, sols))

    print("Static sign-constraint check for singleton-support Tao channels")
    print("Pump: a1^2 -> a2 forces k2 = c2*k1 with c2 in {+2,-2}")
    print("Seed: a1^2 -> a3 forces k3 = c3*k1 with c3 in {+2,-2}")
    print("Amplifier: a2 a3 -> a3 would then require")
    print("  alpha*k3 + beta*k2 + gamma*k3 = 0")
    print("for some alpha,beta,gamma in {+1,-1}.")
    print()

    any_solution = False
    for c2, c3, sols in rows:
        print(f"c2={c2:+d}, c3={c3:+d}, amplifier sign solutions={sols}")
        any_solution = any_solution or bool(sols)

    print()
    print(f"Any solutions? {any_solution}")


if __name__ == "__main__":
    main()
