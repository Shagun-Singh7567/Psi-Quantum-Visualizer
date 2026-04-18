# ψ &nbsp; Psi — Hydrogen Orbital Viewer

An interactive visualizer for the exact quantum mechanical solutions of the hydrogen atom. Explore wavefunctions, probability densities, and three-dimensional orbital shapes across all shells up to n = 3.

**[Live demo → psi-quantum-visualizer.streamlit.app/](https://psi-quantum-visualizer.streamlit.app/)**

---

## Stack

| | |
|---|---|
| **Language** | Python 3.10+ |
| **UI** | Streamlit |
| **Physics** | NumPy · SciPy (Laguerre polynomials, spherical harmonics) |
| **Visualisation** | Plotly |

---

## Running locally

**1. Clone the repo**

```bash
git clone https://github.com/Shagun-Singh7567/psi-quantum-visualizer.git
cd psi-quantum-visualizer
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run**

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser. First load computes and caches each orbital — subsequent selections of the same (n, l, m) are instant.

**Requirements**

```
streamlit>=1.32.0
numpy>=1.26.0
scipy>=1.12.0
plotly>=5.20.0
```

---

## Screenshots
![1s orbital - Radial and Angular nodes](/assets/1sm0_1.png)
![1s orbital - Probability graphs](/assets/1sm0_2.png)
![1s orbital - 3D Visual](/assets/1sm0_3.png)
![2p orbital - Radial and Angular nodes](/assets/2pm0_1.png)
![2p orbital - Probability graphs](/assets/2pm0_2.png)
![2p orbital - 3D Visual](/assets/2pm0_3.png)
![3d orbital - Radial and Angular nodes](/assets/3dm0_1.png)
![3d orbital - Probability graphs](/assets/3dm0_2.png)
![3d orbital - 3D Visual](/assets/3dm0_3.png)k


---

## The Chemistry

The hydrogen atom is the only atom quantum mechanics can solve exactly — one proton, one electron, no approximations needed. The solution is the wavefunction ψ, a function of position that encodes everything physically knowable about the electron. The wavefunction itself isn't directly observable, but its square is: $ψ^2$ at any point in space gives the **probability density** of finding the electron there. This smeared-out cloud of probability is what chemists call an orbital.

Every orbital is defined by three integers — quantum numbers — each controlling a different physical property.

- **n** (principal) sets the energy and overall size. $E_n = -13.6 / n^2$ eV, so larger n means a higher, less tightly bound shell.
- **l** (angular) sets the shape: $l = 0$ is a sphere (s), $l = 1$ is a dumbbell (p), $l = 2$ is a cloverleaf (d).
- **m** (magnetic) sets the orientation in space. For a given $l$ there are $2l + 1$ orientations, all energetically identical without a magnetic field.

The full wavefunction factors cleanly into a radial part and an angular part:

$$\psi_{nlm}(r, \theta, \varphi) = R_{nl}(r) \cdot Y_l^m(\theta, \varphi)$$

$R_{nl}(r)$ controls how the orbital decays with distance from the nucleus. Wherever it crosses zero, there is a **radial node** — a spherical shell where the electron can never be found. The count is $n - l - 1$. $Y_l^m(\theta, \varphi)$ are the spherical harmonics, encoding the directional shape. Their zeros are **angular nodes** — flat planes or cones cutting through the nucleus — and there are exactly $l$ of them.

A useful quantity for chemistry is the radial probability distribution $P(r) = r^2 |R_{nl}(r)|^2$, which answers the question "at what distance from the nucleus is the electron most likely to be?" The $r^2$ factor reflects the growing surface area of larger shells. Its peak shifts outward with $n$, and its mean is $\langle r \rangle = \frac{a_0}{2}[3n^2 - l(l+1)]$, where $a_0 = 0.529$ Å is the Bohr radius.

---

## Visualizations

| Panel | What it shows |
|-------|---------------|
| **Radial R(r)** | Radial wavefunction — zero crossings are radial nodes |
| **Angular \|Y\|²** | Angular probability shape in polar form |
| **XZ / XY / YZ** | $ψ^2$ probability density as 2D cross-sections |
| **P(r)** | Radial probability distribution with $\langle r \rangle$ marked |
| **3D volume** | Full opacity cloud of $ψ^2$ — drag to rotate |