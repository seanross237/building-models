/*
 * integrate_chunk.c
 * SED Hydrogen — Inner RK4 Integration Loop (C implementation)
 * Exploration 002, Strategy 003
 *
 * Implements Landau-Lifshitz ALD:
 *   a = F_C + tau*dF_C/dt + F_zpf + tau*dF_zpf/dt
 *
 * where F_C = -r/|r|^3, dF_C/dt = (-v + 3*r*(r·v/|r|^2)) / |r|^3
 *
 * Compiled with: gcc -O3 -march=native -ffast-math -shared -fPIC -o libsed.so integrate_chunk.c -lm
 */

#include <math.h>
#include <stdlib.h>

/*
 * compute_accel: Landau-Lifshitz acceleration (scalar components).
 */
static inline void compute_accel(
    double px, double py, double pz,
    double vx, double vy, double vz,
    double Fz_x, double Fz_y, double Fz_z,
    double dFz_x, double dFz_y, double dFz_z,
    double tau, double r_soft,
    double *ax, double *ay, double *az)
{
    double r2 = px*px + py*py + pz*pz;
    double r  = sqrt(r2);
    double re = (r < r_soft) ? r_soft : r;
    double r3 = re*re*re;
    double r2e = re*re;

    /* rdv = pos · vel */
    double rdv = px*vx + py*vy + pz*vz;

    /* dF_C/dt = (-vel + 3*pos*(rdv/r^2)) / r^3 */
    double dFC_x = (-vx + 3.0*px*rdv/r2e) / r3;
    double dFC_y = (-vy + 3.0*py*rdv/r2e) / r3;
    double dFC_z = (-vz + 3.0*pz*rdv/r2e) / r3;

    /* a = F_C + tau*dF_C + F_zpf + tau*dF_zpf */
    *ax = -px/r3 + tau*dFC_x + Fz_x + tau*dFz_x;
    *ay = -py/r3 + tau*dFC_y + Fz_y + tau*dFz_y;
    *az = -pz/r3 + tau*dFC_z + Fz_z + tau*dFz_z;
}

/*
 * integrate_chunk: RK4 integration over n_steps timesteps.
 *
 * F_zpf and dF_zpf are (n_steps+1)*3 arrays in row-major order.
 * Row j contains [x, y, z] components at time step j.
 *
 * On input:  (*px_ptr, *py_ptr, *pz_ptr) = current position
 *            (*vx_ptr, *vy_ptr, *vz_ptr) = current velocity
 * On output: updated position and velocity
 *            *steps_done_ptr = number of steps actually taken before ionization
 *                              (= n_steps if no ionization)
 *            *ionized_ptr    = 1 if ionized/nuclear-collision, 0 if not
 */
void integrate_chunk(
    double *px_ptr, double *py_ptr, double *pz_ptr,
    double *vx_ptr, double *vy_ptr, double *vz_ptr,
    const double *F_zpf,    /* (n_steps+1, 3) row-major */
    const double *dF_zpf,   /* (n_steps+1, 3) row-major */
    int n_steps,
    double dt, double tau, double r_soft,
    double r_ion, double r_nuke,
    int *steps_done_ptr, int *ionized_ptr)
{
    double px = *px_ptr, py = *py_ptr, pz = *pz_ptr;
    double vx = *vx_ptr, vy = *vy_ptr, vz = *vz_ptr;

    int ionized = 0;
    int j;

    for (j = 0; j < n_steps; j++) {
        /* Check ionization at current position */
        double r2 = px*px + py*py + pz*pz;
        double r  = sqrt(r2);

        if (r > r_ion || r < r_nuke) {
            ionized = 1;
            break;
        }

        /* Forces at step j and step j+1 (row-major: row j = 3*j) */
        int off_j  = 3 * j;
        int off_j1 = 3 * (j + 1);

        double Fn_x  = F_zpf[off_j];     double Fn_y  = F_zpf[off_j+1];   double Fn_z  = F_zpf[off_j+2];
        double dFn_x = dF_zpf[off_j];    double dFn_y = dF_zpf[off_j+1];  double dFn_z = dF_zpf[off_j+2];
        double Fp_x  = F_zpf[off_j1];    double Fp_y  = F_zpf[off_j1+1];  double Fp_z  = F_zpf[off_j1+2];
        double dFp_x = dF_zpf[off_j1];   double dFp_y = dF_zpf[off_j1+1]; double dFp_z = dF_zpf[off_j1+2];

        /* Half-step interpolation */
        double Fh_x  = 0.5*(Fn_x  + Fp_x);   double Fh_y  = 0.5*(Fn_y  + Fp_y);   double Fh_z  = 0.5*(Fn_z  + Fp_z);
        double dFh_x = 0.5*(dFn_x + dFp_x);  double dFh_y = 0.5*(dFn_y + dFp_y);  double dFh_z = 0.5*(dFn_z + dFp_z);

        /* k1: at (pos, vel), forces at j */
        double a1x, a1y, a1z;
        compute_accel(px, py, pz, vx, vy, vz,
                      Fn_x, Fn_y, Fn_z, dFn_x, dFn_y, dFn_z,
                      tau, r_soft, &a1x, &a1y, &a1z);

        /* k2: at midpoint using k1 slope */
        double p2x = px + 0.5*dt*vx,  p2y = py + 0.5*dt*vy,  p2z = pz + 0.5*dt*vz;
        double v2x = vx + 0.5*dt*a1x, v2y = vy + 0.5*dt*a1y, v2z = vz + 0.5*dt*a1z;
        double a2x, a2y, a2z;
        compute_accel(p2x, p2y, p2z, v2x, v2y, v2z,
                      Fh_x, Fh_y, Fh_z, dFh_x, dFh_y, dFh_z,
                      tau, r_soft, &a2x, &a2y, &a2z);

        /* k3: at midpoint using k2 slope */
        double p3x = px + 0.5*dt*v2x, p3y = py + 0.5*dt*v2y, p3z = pz + 0.5*dt*v2z;
        double v3x = vx + 0.5*dt*a2x, v3y = vy + 0.5*dt*a2y, v3z = vz + 0.5*dt*a2z;
        double a3x, a3y, a3z;
        compute_accel(p3x, p3y, p3z, v3x, v3y, v3z,
                      Fh_x, Fh_y, Fh_z, dFh_x, dFh_y, dFh_z,
                      tau, r_soft, &a3x, &a3y, &a3z);

        /* k4: at next step using k3 slope */
        double p4x = px + dt*v3x, p4y = py + dt*v3y, p4z = pz + dt*v3z;
        double v4x = vx + dt*a3x, v4y = vy + dt*a3y, v4z = vz + dt*a3z;
        double a4x, a4y, a4z;
        compute_accel(p4x, p4y, p4z, v4x, v4y, v4z,
                      Fp_x, Fp_y, Fp_z, dFp_x, dFp_y, dFp_z,
                      tau, r_soft, &a4x, &a4y, &a4z);

        /* Combine RK4 */
        double c = dt / 6.0;
        px += c*(vx  + 2*v2x + 2*v3x + v4x);
        py += c*(vy  + 2*v2y + 2*v3y + v4y);
        pz += c*(vz  + 2*v2z + 2*v3z + v4z);
        vx += c*(a1x + 2*a2x + 2*a3x + a4x);
        vy += c*(a1y + 2*a2y + 2*a3y + a4y);
        vz += c*(a1z + 2*a2z + 2*a3z + a4z);
    }

    *px_ptr = px; *py_ptr = py; *pz_ptr = pz;
    *vx_ptr = vx; *vy_ptr = vy; *vz_ptr = vz;
    *steps_done_ptr = j;
    *ionized_ptr = ionized;
}


/*
 * integrate_chunk_pure_coulomb: Same but with tau=0 and no ZPF.
 * Used for sanity checks.
 */
void integrate_chunk_pure_coulomb(
    double *px_ptr, double *py_ptr, double *pz_ptr,
    double *vx_ptr, double *vy_ptr, double *vz_ptr,
    int n_steps, double dt, double r_soft,
    double *energies_out  /* NULL or preallocated n_steps doubles */
)
{
    double px = *px_ptr, py = *py_ptr, pz = *pz_ptr;
    double vx = *vx_ptr, vy = *vy_ptr, vz = *vz_ptr;

    for (int j = 0; j < n_steps; j++) {
        double r2 = px*px + py*py + pz*pz;
        double r  = sqrt(r2);
        double re = (r < r_soft) ? r_soft : r;

        if (energies_out) {
            double v2 = vx*vx + vy*vy + vz*vz;
            energies_out[j] = 0.5*v2 - 1.0/re;
        }

        double r3 = re*re*re;

        /* k1 */
        double a1x = -px/r3, a1y = -py/r3, a1z = -pz/r3;
        double p2x = px+0.5*dt*vx, p2y = py+0.5*dt*vy, p2z = pz+0.5*dt*vz;
        double v2x = vx+0.5*dt*a1x, v2y = vy+0.5*dt*a1y, v2z = vz+0.5*dt*a1z;

        double _r2 = p2x*p2x+p2y*p2y+p2z*p2z, _r = sqrt(_r2);
        double _re = (_r < r_soft) ? r_soft : _r;
        double _r3 = _re*_re*_re;
        double a2x = -p2x/_r3, a2y = -p2y/_r3, a2z = -p2z/_r3;

        double p3x = px+0.5*dt*v2x, p3y = py+0.5*dt*v2y, p3z = pz+0.5*dt*v2z;
        double v3x = vx+0.5*dt*a2x, v3y = vy+0.5*dt*a2y, v3z = vz+0.5*dt*a2z;
        _r2 = p3x*p3x+p3y*p3y+p3z*p3z; _r = sqrt(_r2);
        _re = (_r < r_soft) ? r_soft : _r; _r3 = _re*_re*_re;
        double a3x = -p3x/_r3, a3y = -p3y/_r3, a3z = -p3z/_r3;

        double p4x = px+dt*v3x, p4y = py+dt*v3y, p4z = pz+dt*v3z;
        double v4x = vx+dt*a3x, v4y = vy+dt*a3y, v4z = vz+dt*a3z;
        _r2 = p4x*p4x+p4y*p4y+p4z*p4z; _r = sqrt(_r2);
        _re = (_r < r_soft) ? r_soft : _r; _r3 = _re*_re*_re;
        double a4x = -p4x/_r3, a4y = -p4y/_r3, a4z = -p4z/_r3;

        double c = dt/6.0;
        px += c*(vx+2*v2x+2*v3x+v4x);
        py += c*(vy+2*v2y+2*v3y+v4y);
        pz += c*(vz+2*v2z+2*v3z+v4z);
        vx += c*(a1x+2*a2x+2*a3x+a4x);
        vy += c*(a1y+2*a2y+2*a3y+a4y);
        vz += c*(a1z+2*a2z+2*a3z+a4z);
    }

    *px_ptr = px; *py_ptr = py; *pz_ptr = pz;
    *vx_ptr = vx; *vy_ptr = vy; *vz_ptr = vz;
}
