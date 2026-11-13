"""
Combined PHYS227 Physics, Step-by-Step Calculus & Engineering Applications Site.

Built using ONLY the CISC108/UD Drafter web framework (`drafter`) and Python's
standard library (`math`, `re`, `dataclasses`)—zero external dependencies.
Splits the site into three interconnected workspaces:
  1. Physics Idea and Applications (Labs 1-9 Solvers & Statistical Error Tools)
  2. Calculus Calculations and Explanations (Step-by-Step Solver & Concept Tutor)
  3. Engineering & Science Applications Info (Calculus in Thermo, Statics, Fluids, Kinetics)
"""

from dataclasses import dataclass
import math
import re
from typing import Any
from drafter import (
    route,
    start_server,
    Page,
    Header,
    Text,
    Button,
    TextBox,
    SelectBox,
    CheckBox,
    TextArea,
    LineBreak,
    HorizontalRule,
    BulletedList,
    Table,
    assert_equal,
    set_website_title,
    set_site_information,
    hide_debug_information,
    set_website_framed,
)

# ==============================================================================
# GITHUB PAGES SITE CONFIGURATION (Step 0)
# ==============================================================================

set_website_title("Where's My Desk")
set_site_information(
    author="Jacob Muzzi",
    description=(
        "Interactive solver and educational reference for PHYS227 Labs 1-9, "
        "step-by-step calculus calculations, and engineering course applications."
    ),
    sources="UDel PHYS227 Lab Manuals (Labs 1-9) and Drafter Documentation.",
    planning=[],
    links=["https://github.com/your-username/your-repository"],
)
hide_debug_information()
set_website_framed(False)


# ==============================================================================
# GLOBAL CONSTANTS (No mutable global variables)
# ==============================================================================

GRAVITY_STD: float = 9.81
GRAVITY_PROJ: float = 9.80

TABLE1_METALS: dict[str, float] = {
    "Magnesium": 1.74,
    "Aluminum": 2.70,
    "Titanium": 4.54,
    "Zinc": 7.13,
    "Chromium": 7.15,
    "Tin": 7.30,
    "Manganese": 7.44,
    "Iron": 7.87,
    "Cadmium": 8.69,
    "Brass": 8.70,
    "Cobalt": 8.86,
    "Nickel": 8.91,
    "Copper": 8.93,
    "Molybdenum": 10.22,
    "Silver": 10.50,
    "Lead": 11.34,
    "Mercury": 13.53,
    "Uranium": 18.95,
    "Tungsten": 19.25,
    "Gold": 19.28,
    "Plutonium": 19.82,
    "Platinum": 21.46,
}

LAB_TOPICS: list[str] = [
    "Lab 1: Unit Conversions & Cylinder Density",
    "Lab 2: Inclined Plane Gravity",
    "Lab 3: 2D Vector Addition & Force Table",
    "Lab 4: Projectile Motion Range",
    "Lab 5: Kinetic Friction Coefficient",
    "Lab 6: Vertical Spring Mechanical Energy",
    "Lab 7: Impulse-Momentum Theorem",
    "Lab 8: Rotational Moment of Inertia",
    "Lab 9: Simple Pendulum & Small Angle",
]

CALCULATION_TYPES: list[str] = [
    "Derivative (d/dx)",
    "Partial Derivative (∂/∂x or ∂/∂y)",
    "Indefinite Integral (∫ f(x) dx)",
    "Definite Integral (∫_a^b f(x) dx)",
    "Double Integral (∬ f(x,y) dx dy)",
    "Limit (lim_{x->a} f(x))",
    "Taylor Series Expansion",
]

TUTOR_TOPICS: list[str] = [
    "Derivatives & Chain Rule",
    "Partial Derivatives",
    "Indefinite & Definite Integrals",
    "Double Integrals (Iterated)",
    "Limits & L'Hopital's Rule",
    "Taylor Series",
]

CONCEPT_GUIDES: dict[str, str] = {
    "Derivatives & Chain Rule": (
        "A derivative measures instantaneous rate of change: f'(x) = lim_{h->0} "
        "[f(x+h) - f(x)] / h. Key rules: Power Rule d/dx[x^n] = n*x^(n-1), "
        "Product Rule (fg)' = f'g + fg', and Chain Rule d/dx[f(g(x))] = f'(g(x))*g'(x)."
    ),
    "Partial Derivatives": (
        "For a multivariable function f(x, y), the partial derivative ∂f/∂x "
        "differentiates with respect to x while treating y (and all other "
        "variables) as constants."
    ),
    "Indefinite & Definite Integrals": (
        "An indefinite integral finds the general antiderivative F(x) + C such "
        "that F'(x) = f(x). A definite integral evaluates net signed area on "
        "[a, b] via the Fundamental Theorem of Calculus: F(b) - F(a)."
    ),
    "Double Integrals (Iterated)": (
        "To compute ∬_R f(x, y) dx dy, evaluate the inner integral with respect "
        "to x first (holding y constant) from x_min to x_max, then integrate the "
        "resulting expression with respect to y from y_min to y_max."
    ),
    "Limits & L'Hopital's Rule": (
        "A limit describes the value f(x) approaches as x -> a. If direct "
        "substitution yields 0/0 or ∞/∞, L'Hopital's Rule states that "
        "lim f(x)/g(x) = lim f'(x)/g'(x)."
    ),
    "Taylor Series": (
        "A Taylor series approximates a smooth function around x = a as an "
        "infinite polynomial: sum_{n=0}^∞ [f^(n)(a) / n!] * (x - a)^n."
    ),
}

CALCULUS_APPLICATIONS_ROWS: list[list[str]] = [
    [
        "Calculus Topic",
        "Real-World Application",
        "Scientific Idea Demonstrated",
    ],
    [
        "Ordinary Derivatives (d/dx, d/dt)",
        "Kinematics (v = dx/dt, a = dv/dt), chemical reaction rates, RC circuit current",
        "Instantaneous rate of change & local conservation laws",
    ],
    [
        "Partial Derivatives (∂f/∂x, ∂f/∂y)",
        "Thermodynamic Maxwell relations, fluid velocity gradients, heat conduction",
        "Sensitivity of a state property when holding other state variables fixed",
    ],
    [
        "Definite Integrals (∫_a^b f(x) dx)",
        "Work done by variable forces/gases (∫ P dV), impulse (∫ F dt), beam deflection",
        "Accumulation of continuous quantities & conservation of energy/momentum",
    ],
    [
        "Double & Surface Integrals (∬ f dA)",
        "Hydrostatic force on submerged dams, center of mass, area moment of inertia",
        "Spatial distribution of pressure, mass, and resistance to bending/rotation",
    ],
    [
        "Limits (lim_{x->a})",
        "Terminal velocity (t -> ∞), continuum hypothesis in fluids (ΔV -> 0)",
        "Asymptotic equilibrium & transition from discrete molecules to continuous media",
    ],
    [
        "Taylor Series Expansions",
        "Small-angle pendulum approximation (sin θ ≈ θ), linearized control systems",
        "Linearization of nonlinear physical systems near stable equilibrium",
    ],
]

ENGINEERING_COURSES: list[str] = [
    "Thermodynamics",
    "Statics",
    "Fluid Mechanics",
    "Kinetics & Dynamics",
    "Mechanics of Materials",
    "Heat Transfer",
]

COURSE_OVERVIEWS: dict[str, dict[str, str]] = {
    "Thermodynamics": {
        "scientific_idea": (
            "Conservation of energy (1st Law) and entropy generation / irreversibility "
            "(2nd Law) across control volumes and closed piston-cylinder systems."
        ),
        "calculus_used": (
            "Definite integrals for boundary work W = ∫ P dV; partial derivatives "
            "for specific heats c_v = (∂u/∂T)_v, c_p = (∂h/∂T)_p, and Maxwell relations."
        ),
        "key_calculations": (
            "• Polytropic Boundary Work: W = (P2*V2 - P1*V1) / (1 - n) (or P1*V1*ln(V2/V1) if n=1)\n"
            "• First Law Closed System: ΔU = Q - W\n"
            "• Entropy Change of Ideal Gas: Δs = c_p * ln(T2/T1) - R * ln(P2/P1)\n"
            "• Carnot Thermal Efficiency: η_max = 1 - (T_cold / T_hot)"
        ),
    },
    "Statics": {
        "scientific_idea": (
            "Static equilibrium of rigid bodies, trusses, and frames where net "
            "external force and net external moment vanish (ΣF = 0, ΣM = 0)."
        ),
        "calculus_used": (
            "Definite & double integrals to find centroids (x̄ = ∫ x dA / ∫ dA), "
            "distributed load resultants F_R = ∫ w(x) dx, and area moments of inertia I = ∫ y² dA."
        ),
        "key_calculations": (
            "• 2D/3D Equilibrium Equations: ΣF_x = 0, ΣF_y = 0, ΣM_O = 0\n"
            "• Distributed Beam Load Resultant: F_R = ∫_0^L w(x) dx acting at x̄\n"
            "• Centroid of Composite Area: x̄ = (Σ x_i * A_i) / (Σ A_i)\n"
            "• Belt Friction Capstan Equation: T_tight = T_slack * e^(μ_s * β)"
        ),
    },
    "Fluid Mechanics": {
        "scientific_idea": (
            "Conservation of mass (Continuity), momentum (Navier-Stokes / Reynolds "
            "Transport Theorem), and mechanical energy (Bernoulli) in flowing fluids."
        ),
        "calculus_used": (
            "Partial derivatives for shear stress τ = μ (∂u/∂y) and velocity fields; "
            "double integrals for volumetric flow rate Q = ∬ (v · n) dA and hydrostatic forces."
        ),
        "key_calculations": (
            "• Hydrostatic Pressure & Dam Force: P = ρ*g*h, F_R = ρ*g*h_c*A\n"
            "• Continuity Equation: ρ1*A1*v1 = ρ2*A2*v2 (or A1*v1 = A2*v2 incompressible)\n"
            "• Bernoulli Energy Equation: P1/(ρg) + v1²/(2g) + z1 = P2/(ρg) + v2²/(2g) + z2 + h_L\n"
            "• Reynolds Number: Re = (ρ * v * D) / μ (Laminar < 2300, Turbulent > 4000)"
        ),
    },
    "Kinetics & Dynamics": {
        "scientific_idea": (
            "Relationship between forces/torques and accelerated motion of particles "
            "and rigid bodies via Newton's 2nd Law, Work-Energy, and Impulse-Momentum."
        ),
        "calculus_used": (
            "Time derivatives v = dr/dt, a = dv/dt, α = dω/dt; chain rule a = v (dv/ds); "
            "definite integrals for work U_{1->2} = ∫ F · dr and impulse J = ∫ F dt."
        ),
        "key_calculations": (
            "• Translational & Rotational Newton's 2nd Law: ΣF = m*a_G, ΣM_G = I_G*α\n"
            "• Principle of Work & Energy: T1 + V1 + U_{1->2,nc} = T2 + V2\n"
            "• Linear & Angular Impulse-Momentum: m*v1 + ∫ F dt = m*v2, I*ω1 + ∫ M dt = I*ω2\n"
            "• Coefficient of Restitution (Impact): e = (v_B2 - v_A2) / (v_A1 - v_B1)"
        ),
    },
    "Mechanics of Materials": {
        "scientific_idea": (
            "Internal stress, strain, and elastic deformation of solid structural "
            "members under axial, torsional, and bending loads."
        ),
        "calculus_used": (
            "Successive integration of distributed load w(x) -> shear V(x) = ∫ w dx -> "
            "bending moment M(x) = ∫ V dx -> beam slope θ(x) -> deflection y(x)."
        ),
        "key_calculations": (
            "• Axial Stress & Elongation: σ = P / A, δ = ∫_0^L [P(x) / (A(x)*E)] dx\n"
            "• Torsional Shear Stress & Twist: τ = (T * r) / J, φ = (T * L) / (J * G)\n"
            "• Flexural Bending Stress: σ_max = -(M * y) / I\n"
            "• Euler-Bernoulli Beam Equation: E * I * (d⁴y / dx⁴) = w(x)"
        ),
    },
    "Heat Transfer": {
        "scientific_idea": (
            "Transport of thermal energy driven by temperature gradients via "
            "conduction (Fourier), convection (Newton), and radiation (Stefan-Boltzmann)."
        ),
        "calculus_used": (
            "Partial differential equations (1D/3D Heat Diffusion Equation ∂T/∂t = α ∂²T/∂x²) "
            "and spatial derivatives for conductive heat flux q'' = -k (dT/dx)."
        ),
        "key_calculations": (
            "• Fourier's Law of Conduction: q_cond = -k * A * (dT / dx)\n"
            "• Newton's Law of Cooling (Convection): q_conv = h * A * (T_s - T_∞)\n"
            "• Stefan-Boltzmann Radiation: q_rad = ε * σ * A * (T_s⁴ - T_surr⁴)\n"
            "• Lumped Capacitance Transient Cooling: (T(t) - T_∞)/(T_i - T_∞) = e^(-t/τ)"
        ),
    },
}

SAFE_MATH_ENV: dict[str, Any] = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "ln": math.log,
    "log": math.log,
    "sqrt": math.sqrt,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
}


# ==============================================================================
# DATACLASSES
# ==============================================================================

@dataclass
class WorkRecord:
    """Represents a single solved Physics or Calculus calculation entry."""

    section: str
    topic: str
    inputs_summary: str
    final_yield: str
    status_note: str


@dataclass
class State:
    """Application state tracking active workspace, settings, and logged entries."""

    active_section: str
    selected_lab: str
    selected_calc_type: str
    selected_tutor_topic: str
    selected_course: str
    show_steps_or_guide: bool
    latest_physics_output: str
    latest_calculus_output: str
    records: list[WorkRecord]


# ==============================================================================
# SECTION 1 HELPER FUNCTIONS: PHYSICS & STATISTICAL ERROR ANALYSIS
# ==============================================================================

def parse_float_list(raw_text: str) -> list[float]:
    """Parse a comma- or space-separated string into a list of floats."""
    cleaned: str = raw_text.replace(",", " ")
    tokens: list[str] = cleaned.split()
    values: list[float] = []
    for token in tokens:
        values.append(float(token))
    return values


def round_phys227(value: float, error: float) -> tuple[str, str]:
    """
    Round a value and its error according to PHYS227 Lab 1 rules:
    1 sig fig for error (2 sig figs if the first non-zero digit is 1).
    """
    abs_err: float = abs(error)
    if abs_err == 0.0:
        return f"{value:.4f}", "0.0"
    order: int = math.floor(math.log10(abs_err))
    first_digit: int = int(abs_err / (10 ** order))
    sig_figs: int = 2 if first_digit == 1 else 1
    decimals: int = -order + (sig_figs - 1)
    rounded_err: float = round(abs_err, decimals)
    rounded_val: float = round(value, decimals)
    if decimals > 0:
        return f"{rounded_val:.{decimals}f}", f"{rounded_err:.{decimals}f}"
    return f"{int(round(rounded_val))}", f"{int(round(rounded_err))}"


def evaluate_discrepancy(
    val_a: float, err_a: float, val_b: float, err_b: float
) -> tuple[float, float, bool]:
    """
    Apply the PHYS227 discrepancy criterion:
    d = |A - B| <= 2 * sqrt(delta_A^2 + delta_B^2).
    """
    diff: float = abs(val_a - val_b)
    combined_err: float = math.sqrt(err_a ** 2 + err_b ** 2)
    threshold: float = 2.0 * combined_err
    agrees: bool = diff <= threshold
    return diff, threshold, agrees


def compute_sample_stats(values: list[float]) -> tuple[float, float]:
    """Compute sample mean and sample standard deviation (N - 1 denominator)."""
    count: int = len(values)
    mean_val: float = sum(values) / count
    sq_diffs: float = 0.0
    for item in values:
        sq_diffs += (item - mean_val) ** 2
    std_dev: float = math.sqrt(sq_diffs / (count - 1))
    return mean_val, std_dev


def identify_matching_metals(density: float, err_density: float) -> list[str]:
    """Return all Table 1 metals whose density agrees within 2*delta_d."""
    matches: list[str] = []
    for metal, std_rho in TABLE1_METALS.items():
        _, _, ok = evaluate_discrepancy(density, err_density, std_rho, 0.01)
        if ok:
            matches.append(f"{metal} ({std_rho:.2f} g/cm³)")
    return matches


def solve_physics_formula(
    lab_name: str,
    p1: float,
    p2: float,
    p3: float,
    p4: float,
) -> tuple[str, str, str]:
    """
    Solve the selected PHYS227 lab calculation given four numeric inputs.
    Returns (inputs_summary, formatted_result, status_note).
    """
    if lab_name == "Lab 1: Unit Conversions & Cylinder Density":
        radius: float = p3 / 2.0
        dr: float = 0.0005
        dh: float = 0.001
        vol: float = math.pi * (radius ** 2) * p4
        dvol: float = vol * math.sqrt((2.0 * dr / radius) ** 2 + (dh / p4) ** 2)
        rho: float = p1 / vol
        drho: float = rho * math.sqrt((p2 / p1) ** 2 + (dvol / vol) ** 2)
        rho_s, drho_s = round_phys227(rho, drho)
        metals: list[str] = identify_matching_metals(rho, drho)
        metal_txt: str = ", ".join(metals) if metals else "None in Table 1"
        summary: str = f"m={p1}g, d={p3}cm, h={p4}cm"
        res: str = f"ρ = ({rho_s} ± {drho_s}) g/cm³ | Matches: {metal_txt}"
        status: str = "Matched Metal" if metals else "No Match"
        return summary, res, status

    if lab_name == "Lab 2: Inclined Plane Gravity":
        sin_theta: float = p1 / p2
        g_exp: float = p3 / sin_theta
        _, _, ok = evaluate_discrepancy(g_exp, p4, GRAVITY_STD, 0.03)
        summary = f"h={p1}m, d={p2}m, a={p3}m/s²"
        res = f"g = ({g_exp:.3f} ± {p4:.3f}) m/s² (Agrees w/ 9.81: {ok})"
        return summary, res, "In Agreement" if ok else "Discrepancy"

    if lab_name == "Lab 3: 2D Vector Addition & Force Table":
        f1: float = (p1 / 1000.0) * GRAVITY_STD
        f2: float = (p3 / 1000.0) * GRAVITY_STD
        fx: float = f1 * math.cos(math.radians(p2)) + f2 * math.cos(math.radians(p4))
        fy: float = f1 * math.sin(math.radians(p2)) + f2 * math.sin(math.radians(p4))
        f_net: float = math.hypot(fx, fy)
        eq_ang: float = (math.degrees(math.atan2(fy, fx)) + 180.0) % 360.0
        eq_mass: float = (f_net / GRAVITY_STD) * 1000.0
        summary = f"m1={p1}g@{p2}°, m2={p3}g@{p4}°"
        res = f"Equilibrant: {eq_mass:.2f} g at {eq_ang:.2f}° CCW (F_net={f_net:.4f} N)"
        return summary, res, "Balanced"

    if lab_name == "Lab 4: Projectile Motion Range":
        v0: float = math.sqrt(2.0 * GRAVITY_PROJ * max(0.0, p2 - p1))
        x_pred: float = v0 * math.sqrt(2.0 * p3 / GRAVITY_PROJ)
        _, _, ok = evaluate_discrepancy(p4, 0.02, x_pred, 0.03)
        summary = f"Δy={p2 - p1:.3f}m, h={p3}m, x_meas={p4}m"
        res = f"v0={v0:.3f} m/s | x_pred={x_pred:.4f} m vs x_meas={p4:.4f} m (Agrees: {ok})"
        return summary, res, "In Agreement" if ok else "Discrepancy"

    if lab_name == "Lab 5: Kinetic Friction Coefficient":
        rad: float = math.radians(p4)
        f_k: float = (
            p2 * GRAVITY_STD
            - (p1 + p2) * p3
            - p1 * GRAVITY_STD * math.sin(rad)
        )
        normal: float = p1 * GRAVITY_STD * math.cos(rad)
        mu_k: float = f_k / normal
        summary = f"mt={p1}kg, mh={p2}kg, a={p3}m/s², θ={p4}°"
        res = f"μ_k = {mu_k:.4f} (f_k = {f_k:.4f} N, N = {normal:.4f} N)"
        return summary, res, "Valid μ_k" if mu_k >= 0.0 else "Check Inputs"

    if lab_name == "Lab 6: Vertical Spring Mechanical Energy":
        mass: float = 0.100
        k_en: float = 0.5 * mass * (p4 ** 2)
        ug_en: float = mass * GRAVITY_STD * p3
        us_en: float = 0.5 * p1 * ((p3 - p2) ** 2)
        e_tot: float = k_en + ug_en + us_en
        summary = f"k={p1}N/m, ys={p2}m, y={p3}m, v={p4}m/s"
        res = f"E_tot = {e_tot:.5f} J (K={k_en:.4f}, Ug={ug_en:.4f}, Us={us_en:.4f})"
        return summary, res, "Conserved"

    if lab_name == "Lab 7: Impulse-Momentum Theorem":
        dp: float = p1 * (p3 - p2)
        _, _, ok = evaluate_discrepancy(dp, 0.015, p4, 0.015)
        summary = f"m={p1}kg, vi={p2}m/s, vf={p3}m/s, J={p4}N·s"
        res = f"Δp = {dp:.4f} N·s vs J = {p4:.4f} N·s (Agrees: {ok})"
        return summary, res, "In Agreement" if ok else "Discrepancy"

    if lab_name == "Lab 8: Rotational Moment of Inertia":
        i_disk: float = 0.5 * p1 * ((p2 / 2.0) ** 2)
        i_plate: float = (1.0 / 12.0) * p3 * (0.075 ** 2 + p4 ** 2)
        summary = f"m_d={p1}kg, D={p2}m, m_p={p3}kg, L={p4}m"
        res = f"I_disk = {i_disk:.6e} kg·m² | I_plate = {i_plate:.6e} kg·m²"
        return summary, res, "Computed"

    # Lab 9: Simple Pendulum & Small Angle
    g_pend: float = (4.0 * (math.pi ** 2) * p1) / (p2 ** 2)
    rad_amp: float = math.radians(p3)
    pct_shift: float = ((1.0 / 16.0) * (rad_amp ** 2)) * 100.0
    _, _, ok = evaluate_discrepancy(g_pend, p4, GRAVITY_STD, 0.03)
    summary = f"L={p1}m, T={p2}s, θ={p3}°"
    res = f"g = ({g_pend:.3f} ± {p4:.3f}) m/s² | Small-angle shift: +{pct_shift:.3f}%"
    return summary, res, "In Agreement" if ok else "Discrepancy"


# ==============================================================================
# SECTION 2 HELPER FUNCTIONS: PURE-PYTHON SYMBOLIC & NUMERICAL CALCULUS ENGINE
# ==============================================================================

def normalize_expr_string(expr_text: str) -> str:
    """
    Convert user math notation (like 3x^2 + 4x - 5) into valid Python syntax
    (3*x**2 + 4*x - 5).
    """
    cleaned: str = expr_text.strip().replace("^", "**")
    cleaned = re.sub(r"(\d)([a-zA-Z\(])", r"\1*\2", cleaned)
    cleaned = re.sub(r"([xy])([xy\(])", r"\1*\2", cleaned)
    return cleaned


def eval_math_at(expr_text: str, x_val: float, y_val: float = 0.0) -> float:
    """Safely evaluate a math expression string at numerical (x, y) coordinates."""
    py_expr: str = normalize_expr_string(expr_text)
    local_vars: dict[str, Any] = dict(SAFE_MATH_ENV)
    local_vars["x"] = x_val
    local_vars["y"] = y_val
    return float(eval(py_expr, {"__builtins__": {}}, local_vars))


def parse_monomial_terms(expr_text: str) -> list[tuple[float, int, int]] | None:
    """
    Parse a polynomial in x and y into a list of (coeff, x_pow, y_pow) tuples.
    Returns None if the expression contains non-polynomial functions (e.g., sin).
    """
    compact: str = expr_text.replace(" ", "").replace("**", "^")
    if not compact:
        return None
    if compact[0] not in "+-":
        compact = "+" + compact
    raw_terms: list[str] = re.findall(r"[+-][^+-]+", compact)
    if "".join(raw_terms) != compact:
        return None

    parsed: list[tuple[float, int, int]] = []
    pattern = re.compile(
        r"^([+-]?\d*\.?\d*)\*?"
        r"(?:(x)(?:\^(\d+))?)?\*?"
        r"(?:(y)(?:\^(\d+))?)?$"
    )
    for term in raw_terms:
        match = pattern.match(term)
        if not match:
            return None
        c_str, has_x, x_exp_s, has_y, y_exp_s = match.groups()
        if c_str in ("", "+"):
            coeff: float = 1.0
        elif c_str == "-":
            coeff = -1.0
        else:
            coeff = float(c_str)
        x_pow: int = int(x_exp_s) if x_exp_s else (1 if has_x else 0)
        y_pow: int = int(y_exp_s) if y_exp_s else (1 if has_y else 0)
        parsed.append((coeff, x_pow, y_pow))
    return parsed


def format_polynomial(terms: list[tuple[float, int, int]]) -> str:
    """Format a list of (coeff, x_pow, y_pow) monomials into clean algebra text."""
    pieces: list[str] = []
    for coeff, x_pow, y_pow in terms:
        if abs(coeff) < 1e-12:
            continue
        sign: str = " - " if coeff < 0 else (" + " if pieces else "")
        mag: float = abs(coeff)
        mag_s: str = f"{int(mag)}" if mag.is_integer() else f"{mag:.4g}"
        var_part: str = ""
        if x_pow == 1:
            var_part += "x"
        elif x_pow > 1:
            var_part += f"x^{x_pow}"
        if y_pow == 1:
            var_part += ("*y" if var_part else "y")
        elif y_pow > 1:
            var_part += (f"*y^{y_pow}" if var_part else f"y^{y_pow}")
        if not var_part:
            pieces.append(f"{sign}{mag_s}")
        elif mag_s == "1":
            pieces.append(f"{sign}{var_part}")
        else:
            pieces.append(f"{sign}{mag_s}*{var_part}")
    return "".join(pieces) if pieces else "0"


def eval_polynomial(
    terms: list[tuple[float, int, int]], x_val: float, y_val: float = 0.0
) -> float:
    """Evaluate a parsed monomial list at (x_val, y_val)."""
    total: float = 0.0
    for coeff, x_pow, y_pow in terms:
        total += coeff * (x_val ** x_pow) * (y_val ** y_pow)
    return total


def simpson_1d(expr_text: str, a_val: float, b_val: float, n_steps: int = 200) -> float:
    """Compute a high-accuracy 1D definite integral using Composite Simpson's Rule."""
    h_step: float = (b_val - a_val) / n_steps
    total: float = eval_math_at(expr_text, a_val) + eval_math_at(expr_text, b_val)
    for idx in range(1, n_steps):
        weight: float = 4.0 if idx % 2 == 1 else 2.0
        total += weight * eval_math_at(expr_text, a_val + idx * h_step)
    return total * (h_step / 3.0)


def compute_derivative_steps(
    expr_text: str, var_name: str, order: int
) -> tuple[str, str]:
    """Compute ordinary or partial derivatives with symbolic polynomial breakdown."""
    steps: list[str] = [
        f"Step 1: Parse target function f = {expr_text} and variable '{var_name}'.",
    ]
    if var_name == "y":
        steps.append("Step 2: Hold 'x' constant and apply Power Rule d/dy[y^n] = n*y^(n-1).")
    else:
        steps.append("Step 2: Hold any other variables constant and apply Power Rule.")

    terms = parse_monomial_terms(expr_text)
    if terms is not None:
        curr_terms: list[tuple[float, int, int]] = terms
        for step_idx in range(1, order + 1):
            next_terms: list[tuple[float, int, int]] = []
            for coeff, x_pow, y_pow in curr_terms:
                if var_name == "x" and x_pow > 0:
                    next_terms.append((coeff * x_pow, x_pow - 1, y_pow))
                elif var_name == "y" and y_pow > 0:
                    next_terms.append((coeff * y_pow, x_pow, y_pow - 1))
            curr_terms = next_terms
            res_str: str = format_polynomial(curr_terms)
            steps.append(f"Step 3.{step_idx}: Order {step_idx} derivative = {res_str}")
        final_yield: str = format_polynomial(curr_terms)
        steps.append(f"Final Yield: {final_yield}")
        return "\n".join(steps), final_yield

    h_diff: float = 1e-5
    x0: float = 1.0
    deriv_at_1: float = (
        eval_math_at(expr_text, x0 + h_diff) - eval_math_at(expr_text, x0 - h_diff)
    ) / (2.0 * h_diff)
    steps.append(
        f"Step 3: Non-polynomial expression; central-difference slope at x=1 is "
        f"f'(1) ≈ {deriv_at_1:.6f}."
    )
    final_yield = f"f'(1) ≈ {deriv_at_1:.6f}"
    steps.append(f"Final Yield: {final_yield}")
    return "\n".join(steps), final_yield


def compute_integral_steps(
    expr_text: str, calc_type: str, params: list[float]
) -> tuple[str, str]:
    """Compute indefinite, definite, or double integrals with intermediate steps."""
    steps: list[str] = [f"Step 1: Parse integrand f = {expr_text}."]
    terms = parse_monomial_terms(expr_text)

    if calc_type == "Indefinite Integral (∫ f(x) dx)":
        if terms is not None:
            anti_terms: list[tuple[float, int, int]] = []
            for coeff, x_pow, y_pow in terms:
                anti_terms.append((coeff / (x_pow + 1), x_pow + 1, y_pow))
            anti_str: str = format_polynomial(anti_terms)
            final_yield: str = f"{anti_str} + C"
            steps.append("Step 2: Apply Power Rule ∫ x^n dx = x^(n+1)/(n+1) term-by-term.")
            steps.append(f"Step 3: Add constant of integration C: {final_yield}")
            steps.append(f"Final Yield: {final_yield}")
            return "\n".join(steps), final_yield
        steps.append("Step 2: General transcendental antiderivative evaluated numerically.")
        return "\n".join(steps), f"∫({expr_text}) dx + C"

    if calc_type == "Definite Integral (∫_a^b f(x) dx)":
        a_val: float = params[0] if len(params) >= 1 else 0.0
        b_val: float = params[1] if len(params) >= 2 else 1.0
        if terms is not None:
            anti_terms = [
                (coeff / (x_pow + 1), x_pow + 1, y_pow)
                for coeff, x_pow, y_pow in terms
            ]
            anti_str = format_polynomial(anti_terms)
            f_b: float = eval_polynomial(anti_terms, b_val)
            f_a: float = eval_polynomial(anti_terms, a_val)
            net_area: float = f_b - f_a
            final_yield = (
                f"{int(round(net_area))}"
                if abs(net_area - round(net_area)) < 1e-9
                else f"{net_area:.6g}"
            )
            steps.append(f"Step 2: Antiderivative F(x) = {anti_str}.")
            steps.append(
                f"Step 3: Fundamental Theorem F({b_val}) - F({a_val}) = "
                f"{f_b:.6g} - {f_a:.6g} = {final_yield}."
            )
            steps.append(f"Final Yield: {final_yield}")
            return "\n".join(steps), final_yield

        num_area: float = simpson_1d(expr_text, a_val, b_val)
        final_yield = f"{num_area:.6g}"
        steps.append(
            f"Step 2: Apply Composite Simpson's Rule on [{a_val}, {b_val}]: {final_yield}."
        )
        steps.append(f"Final Yield: {final_yield}")
        return "\n".join(steps), final_yield

    # Double Integral: ∬ f(x, y) dx dy over [x0, x1] x [y0, y1]
    x0: float = params[0] if len(params) >= 1 else 0.0
    x1: float = params[1] if len(params) >= 2 else 1.0
    y0: float = params[2] if len(params) >= 3 else 0.0
    y1: float = params[3] if len(params) >= 4 else 1.0

    if terms is not None:
        inner_y_terms: list[tuple[float, int, int]] = []
        for coeff, x_pow, y_pow in terms:
            new_c: float = (coeff / (x_pow + 1)) * (x1 ** (x_pow + 1) - x0 ** (x_pow + 1))
            inner_y_terms.append((new_c, 0, y_pow))
        inner_str: str = format_polynomial(inner_y_terms)

        outer_y_terms: list[tuple[float, int, int]] = [
            (coeff / (y_pow + 1), 0, y_pow + 1)
            for coeff, _, y_pow in inner_y_terms
        ]
        vol_val: float = eval_polynomial(outer_y_terms, 0.0, y1) - eval_polynomial(
            outer_y_terms, 0.0, y0
        )
        final_yield = (
            f"{int(round(vol_val))}"
            if abs(vol_val - round(vol_val)) < 1e-9
            else f"{vol_val:.6g}"
        )
        steps.append(
            f"Step 2 (Inner Integral w.r.t. x from {x0} to {x1}): g(y) = {inner_str}"
        )
        steps.append(
            f"Step 3 (Outer Integral w.r.t. y from {y0} to {y1}): "
            f"G({y1}) - G({y0}) = {final_yield}"
        )
        steps.append(f"Final Yield: {final_yield}")
        return "\n".join(steps), final_yield

    steps.append("Step 2: Non-polynomial 2D integrand requires polynomial input.")
    return "\n".join(steps), "Unsupported Form"


def solve_calculus_query(
    calc_type: str, expr_text: str, param_text: str
) -> tuple[str, str]:
    """
    Dispatch any supported calculus operation and return (steps_text, final_yield).
    Handles invalid syntax gracefully without external libraries.
    """
    try:
        params: list[float] = parse_float_list(
            param_text.replace("x", "0").replace("y", "1")
        )
    except ValueError as exc:
        return f"Parameter Parse Error: {exc}", "Invalid Input"

    try:
        if calc_type == "Derivative (d/dx)":
            order: int = int(params[0]) if len(params) >= 1 else 1
            return compute_derivative_steps(expr_text, "x", max(1, order))

        if calc_type == "Partial Derivative (∂/∂x or ∂/∂y)":
            var_choice: str = "y" if "y" in param_text.lower() else "x"
            return compute_derivative_steps(expr_text, var_choice, 1)

        if "Integral" in calc_type:
            return compute_integral_steps(expr_text, calc_type, params)

        if calc_type == "Limit (lim_{x->a} f(x))":
            point_a: float = params[0] if len(params) >= 1 else 0.0
            left_val: float = eval_math_at(expr_text, point_a - 1e-6)
            right_val: float = eval_math_at(expr_text, point_a + 1e-6)
            avg_lim: float = 0.5 * (left_val + right_val)
            clean_lim: str = (
                f"{int(round(avg_lim))}"
                if abs(avg_lim - round(avg_lim)) < 1e-5
                else f"{avg_lim:.6g}"
            )
            steps: list[str] = [
                f"Step 1: Evaluate two-sided limit of f(x) = {expr_text} as x -> {point_a}.",
                f"Step 2: Left approach f({point_a}-1e-6) = {left_val:.6f} | "
                f"Right approach f({point_a}+1e-6) = {right_val:.6f}.",
                f"Final Yield: {clean_lim}",
            ]
            return "\n".join(steps), clean_lim

        # Taylor Series Expansion around x = a up to degree n
        center_a: float = params[0] if len(params) >= 1 else 0.0
        degree_n: int = int(params[1]) if len(params) >= 2 else 2
        h_step: float = 1e-3
        f0: float = eval_math_at(expr_text, center_a)
        f1: float = (
            eval_math_at(expr_text, center_a + h_step)
            - eval_math_at(expr_text, center_a - h_step)
        ) / (2.0 * h_step)
        f2: float = (
            eval_math_at(expr_text, center_a + h_step)
            - 2.0 * f0
            + eval_math_at(expr_text, center_a - h_step)
        ) / (h_step ** 2)
        poly_str: str = (
            f"{f0:.4g} + ({f1:.4g})*(x - {center_a}) + ({f2/2.0:.4g})*(x - {center_a})^2"
        )
        t_steps: list[str] = [
            f"Step 1: Expand f(x) = {expr_text} around center a = {center_a} (degree {degree_n}).",
            f"Step 2: f(a)={f0:.4g}, f'(a)={f1:.4g}, f''(a)={f2:.4g}.",
            f"Final Yield: {poly_str}",
        ]
        return "\n".join(t_steps), poly_str
    except Exception as exc:
        return f"Calculation Error: {exc}", "Invalid Expression"


def build_navigation_bar() -> list[Any]:
    """Create shared top navigation buttons across all workspaces."""
    return [
        Button("Home / Overview", "/"),
        Button("1. Physics Idea and Applications", "/physics"),
        Button("2. Calculus Calculations and Explanations", "/calculus"),
        Button("3. Engineering & Science Applications Info", "/applications"),
        Button("Combined Session Report Log", "/log"),
        HorizontalRule(),
    ]


# ==============================================================================
# ROUTES (11 ROUTES & 6 DISTINCT PAGES)
# ==============================================================================

@route
def index(state: State) -> Page:
    """Render the landing page introducing all workspaces on the site."""
    state.active_section = "Overview"
    return Page(
        state,
        [
            Header("PHYS227, Calculus & Engineering Science Platform"),
            Text(
                "Explore experimental physics labs, step-by-step symbolic calculus "
                "derivations, and real-world engineering course applications."
            ),
            LineBreak(),
            *build_navigation_bar(),
            Header("Site Workspaces", 2),
            BulletedList(
                [
                    "Section 1 — Physics Idea and Applications: PHYS227 Labs 1–9 "
                    "solvers, repeated-trial sample statistics, PHYS227 error rounding, "
                    "and 2-sigma discrepancy verification.",
                    "Section 2 — Calculus Calculations and Explanations: Dropdown "
                    "solver for Derivatives, Partial Derivatives, Integrals, "
                    "Double Integrals, Limits, and Taylor Series with full intermediate "
                    "steps and conceptual theorem explanations.",
                    "Section 3 — Engineering & Science Applications Info: How calculus "
                    "demonstrates core scientific ideas across Thermodynamics, Statics, "
                    "Fluid Mechanics, Kinetics & Dynamics, Mechanics of Materials, and "
                    "Heat Transfer.",
                    f"Total Logged Calculations in Current Session: {len(state.records)}",
                ]
            ),
        ],
    )


@route
def physics(state: State) -> Page:
    """Render Section 1: Physics Idea and Applications (Labs 1-9 & Error Analysis)."""
    state.active_section = "Physics Idea and Applications"
    guide_text: str = ""
    if state.show_steps_or_guide:
        guide_text = (
            "Parameter Guide: Lab 1 (m[g], dm[g], d[cm], h[cm]) | "
            "Lab 2 (h[m], d[m], a[m/s²], δg) | Lab 3 (m1[g], θ1°, m2[g], θ2°) | "
            "Lab 4 (y0[m], ymax[m], h[m], x_meas[m]) | Lab 5 (mt[kg], mh[kg], a, θ°) | "
            "Lab 6 (k, ys[m], y[m], v[m/s]) | Lab 7 (m[kg], vi, vf, J) | "
            "Lab 8 (m_disk, D_disk, m_plate, L_plate) | Lab 9 (L[m], T[s], θ°, δg)"
        )

    return Page(
        state,
        [
            Header("Section 1: Physics Idea and Applications"),
            *build_navigation_bar(),
            Header("A. PHYS227 Lab Solvers (Labs 1–9)", 3),
            Text("Select Lab Module:"),
            SelectBox("selected_lab", LAB_TOPICS, state.selected_lab),
            LineBreak(),
            CheckBox("show_steps_or_guide", state.show_steps_or_guide),
            Text("Show Parameter Guide"),
            LineBreak(),
            Text(guide_text),
            LineBreak(),
            Text("Parameter 1:"),
            TextBox("p1_str", "0.052"),
            Text("Parameter 2:"),
            TextBox("p2_str", "1.000"),
            Text("Parameter 3:"),
            TextBox("p3_str", "0.505"),
            Text("Parameter 4:"),
            TextBox("p4_str", "0.150"),
            LineBreak(),
            Button("Solve Physics Application & Log", "/solve_physics"),
            HorizontalRule(),
            Header("B. Repeated Trials & Discrepancy Error Analysis", 3),
            Text("Repeated Trial Values (comma- or space-separated):"),
            TextArea("trials_text", "5.02, 4.96, 5.05, 4.98, 5.01"),
            Text("Units:"),
            TextBox("units_str", "s"),
            Text("Cycle Divisor (1 for single events, 5 or 10 for beat intervals):"),
            TextBox("divisor_str", "1"),
            Button("Compute Trial Mean, Std Dev & PHYS227 Rounding", "/solve_trials"),
            HorizontalRule(),
            Header("Latest Physics & Error Output", 3),
            TextArea("phys_out", state.latest_physics_output, rows=4, cols=85),
        ],
    )


@route
def solve_physics(
    state: State,
    selected_lab: str,
    show_steps_or_guide: bool,
    p1_str: str,
    p2_str: str,
    p3_str: str,
    p4_str: str,
) -> Page:
    """Process physics lab inputs, update State fields, and log a WorkRecord."""
    state.selected_lab = selected_lab
    state.show_steps_or_guide = show_steps_or_guide
    p1: float = float(p1_str)
    p2: float = float(p2_str)
    p3: float = float(p3_str)
    p4: float = float(p4_str)

    summary, result_txt, status = solve_physics_formula(
        selected_lab, p1, p2, p3, p4
    )
    state.latest_physics_output = f"[{selected_lab}]\n{result_txt}"
    state.records.append(
        WorkRecord(
            section="Physics Idea and Applications",
            topic=selected_lab,
            inputs_summary=summary,
            final_yield=result_txt,
            status_note=status,
        )
    )
    return physics(state)


@route
def solve_trials(
    state: State, trials_text: str, units_str: str, divisor_str: str
) -> Page:
    """Compute sample mean, sample std dev, and PHYS227 rounded uncertainty."""
    values: list[float] = parse_float_list(trials_text)
    divisor: int = max(1, int(divisor_str))
    mean_raw, std_raw = compute_sample_stats(values)
    per_val: float = mean_raw / divisor
    per_err: float = std_raw / divisor
    val_s, err_s = round_phys227(per_val, per_err)

    result_txt: str = (
        f"N={len(values)} | Mean={mean_raw:.5f}, StdDev={std_raw:.5f} | "
        f"Reported: ({val_s} ± {err_s}) {units_str}"
    )
    state.latest_physics_output = result_txt
    state.records.append(
        WorkRecord(
            section="Physics Idea and Applications",
            topic="Repeated Trials & Error Analysis",
            inputs_summary=f"N={len(values)}, divisor={divisor}",
            final_yield=result_txt,
            status_note="Rounded per Lab 1",
        )
    )
    return physics(state)


@route
def calculus(state: State) -> Page:
    """Render Section 2: Calculus Calculations and Explanations."""
    state.active_section = "Calculus Calculations and Explanations"
    concept_explanation: str = CONCEPT_GUIDES.get(
        state.selected_tutor_topic,
        "Select a calculus concept below to read its theorem and strategy.",
    )
    return Page(
        state,
        [
            Header("Section 2: Calculus Calculations and Explanations"),
            *build_navigation_bar(),
            Header("A. Step-by-Step Calculus Solver", 3),
            Text("1. Choose Calculation Type:"),
            SelectBox(
                "selected_calc_type",
                CALCULATION_TYPES,
                state.selected_calc_type,
            ),
            LineBreak(),
            Text("2. Enter Function f(x) or f(x, y) (e.g., 3*x^2 + 4*x - 5 or x + y):"),
            TextBox("expr_input", "3*x^2 + 4*x - 5"),
            LineBreak(),
            Text(
                "3. Enter Bounds / Variable / Order (comma-separated): "
                "[Derivative order: 1 or 2 | Partial var: x or y | "
                "Definite bounds: 0, 2 | Double bounds x0,x1,y0,y1: 0, 1, 0, 2 | "
                "Limit point: 0 | Taylor center,degree: 0, 2]"
            ),
            TextBox("param_input", "1"),
            LineBreak(),
            CheckBox("show_steps_or_guide", state.show_steps_or_guide),
            Text("Show Intermediate Calculation Steps"),
            LineBreak(),
            Button("Calculate & Show Steps", "/solve_calculus"),
            HorizontalRule(),
            Header("Step-by-Step Calculation & Final Yield", 3),
            TextArea("calc_out", state.latest_calculus_output, rows=9, cols=85),
            HorizontalRule(),
            Header("B. Calculus Concept & Theorem Explanations", 3),
            Text("Select Concept to Explain:"),
            SelectBox(
                "selected_tutor_topic",
                TUTOR_TOPICS,
                state.selected_tutor_topic,
            ),
            Button("Load Concept Explanation", "/explain_calculus"),
            LineBreak(),
            Text(f"[{state.selected_tutor_topic}] {concept_explanation}"),
        ],
    )


@route
def solve_calculus(
    state: State,
    selected_calc_type: str,
    expr_input: str,
    param_input: str,
    show_steps_or_guide: bool,
) -> Page:
    """Compute the requested calculus problem with steps, update State, and log."""
    state.selected_calc_type = selected_calc_type
    state.show_steps_or_guide = show_steps_or_guide

    steps_text, final_yield = solve_calculus_query(
        selected_calc_type, expr_input, param_input
    )

    if state.show_steps_or_guide:
        state.latest_calculus_output = (
            f"Calculation Mode: {selected_calc_type}\n"
            f"Expression: {expr_input} | Parameters: {param_input or 'Default'}\n"
            f"{'-' * 55}\n"
            f"{steps_text}"
        )
    else:
        state.latest_calculus_output = (
            f"[{selected_calc_type}] f = {expr_input}  ==>  Final Yield: {final_yield}"
        )

    state.records.append(
        WorkRecord(
            section="Calculus Calculations and Explanations",
            topic=selected_calc_type,
            inputs_summary=f"f={expr_input} ({param_input or 'default'})",
            final_yield=final_yield,
            status_note="Solved",
        )
    )
    return calculus(state)


@route
def explain_calculus(state: State, selected_tutor_topic: str) -> Page:
    """Update the selected calculus explanation topic in State and re-render."""
    state.selected_tutor_topic = selected_tutor_topic
    return calculus(state)


@route
def applications(state: State) -> Page:
    """
    Render Section 3: Information page covering calculus applications,
    demonstrated scientific ideas, and engineering course overviews.
    """
    state.active_section = "Engineering & Science Applications Info"
    course_data: dict[str, str] = COURSE_OVERVIEWS.get(
        state.selected_course, COURSE_OVERVIEWS["Thermodynamics"]
    )
    return Page(
        state,
        [
            Header("Section 3: Calculus Applications & Engineering Science Overview"),
            *build_navigation_bar(),
            Header("A. How Calculus Demonstrates Core Scientific Ideas", 3),
            Text(
                "Every calculus operation models a fundamental physical principle—from "
                "instantaneous rates of change to spatial conservation laws:"
            ),
            LineBreak(),
            Table(CALCULUS_APPLICATIONS_ROWS),
            HorizontalRule(),
            Header("B. Engineering & Physics Course Calculation Quick-Guide", 3),
            Text("Choose an Engineering or Science Course:"),
            SelectBox(
                "selected_course",
                ENGINEERING_COURSES,
                state.selected_course,
            ),
            Button("Inspect Course Formulas & Concepts", "/select_engineering_course"),
            LineBreak(),
            Header(f"{state.selected_course} — Core Principles & Calculations", 3),
            Text(f"Scientific Idea Demonstrated: {course_data['scientific_idea']}"),
            LineBreak(),
            Text(f"Role of Calculus: {course_data['calculus_used']}"),
            LineBreak(),
            TextArea(
                "course_formulas_box",
                course_data["key_calculations"],
                rows=6,
                cols=85,
            ),
        ],
    )


@route
def select_engineering_course(state: State, selected_course: str) -> Page:
    """Update the selected engineering course in State and re-render info page."""
    state.selected_course = selected_course
    return applications(state)


@route
def log(state: State) -> Page:
    """Render the Combined Session Report Log iterating over all WorkRecords."""
    state.active_section = "Combined Report Log"
    table_rows: list[list[str]] = [
        ["Section", "Topic / Mode", "Inputs", "Final Yield", "Status"]
    ]
    physics_count: int = 0
    calculus_count: int = 0

    # Loop meaningfully iterating over attributes of list[WorkRecord]
    for rec in state.records:
        if rec.section == "Physics Idea and Applications":
            physics_count += 1
        else:
            calculus_count += 1
        table_rows.append(
            [
                rec.section,
                rec.topic,
                rec.inputs_summary,
                rec.final_yield,
                rec.status_note,
            ]
        )

    summary_text: str = (
        f"Combined Report Summary: {len(state.records)} total entries logged "
        f"({physics_count} in 'Physics Idea and Applications', "
        f"{calculus_count} in 'Calculus Calculations and Explanations')."
    )

    return Page(
        state,
        [
            Header("Combined Session Report Log"),
            *build_navigation_bar(),
            Text(summary_text),
            LineBreak(),
            Table(table_rows),
            LineBreak(),
            Button("Clear All Logged Records", "/clear_log"),
        ],
    )


@route
def clear_log(state: State) -> Page:
    """Clear all logged WorkRecord entries from State."""
    state.records = []
    state.latest_physics_output = "Log cleared. Ready for new physics calculations."
    state.latest_calculus_output = "Log cleared. Ready for new calculus problems."
    return log(state)


# ==============================================================================
# UNIT TESTS (Covering Helper Functions and All 11 Routes)
# ==============================================================================

def run_all_tests() -> None:
    """Execute comprehensive unit tests on all physics/calculus helpers and routes."""
    # Physics & statistics helper tests
    assert_equal(round_phys227(5.466, 0.252), ("5.5", "0.3"))
    assert_equal(evaluate_discrepancy(107.0, 2.0, 115.0, 3.0)[2], False)
    assert_equal(evaluate_discrepancy(9.78, 0.14, 9.81, 0.03)[2], True)
    mean_v, std_v = compute_sample_stats([5.2, 5.7, 5.5])
    assert_equal(round(mean_v, 3), 5.467)
    assert_equal(round(std_v, 3), 0.252)

    # Calculus helper tests (pure-Python engine)
    _, d_res = solve_calculus_query("Derivative (d/dx)", "x^3 + 2*x", "1")
    assert_equal(d_res, "3*x^2 + 2")
    _, pd_res = solve_calculus_query(
        "Partial Derivative (∂/∂x or ∂/∂y)", "x^2*y^3", "y"
    )
    assert_equal(pd_res, "3*x^2*y^2")
    _, indef_res = solve_calculus_query(
        "Indefinite Integral (∫ f(x) dx)", "3*x^2", ""
    )
    assert_equal(indef_res, "x^3 + C")
    _, int_res = solve_calculus_query(
        "Definite Integral (∫_a^b f(x) dx)", "2*x", "0, 3"
    )
    assert_equal(int_res, "9")
    _, dbl_res = solve_calculus_query(
        "Double Integral (∬ f(x,y) dx dy)", "x + y", "0, 1, 0, 2"
    )
    assert_equal(dbl_res, "3")
    _, lim_res = solve_calculus_query(
        "Limit (lim_{x->a} f(x))", "sin(x)/x", "0"
    )
    assert_equal(lim_res, "1")

    # Route unit tests (all 11 routes)
    test_state: State = State(
        active_section="Overview",
        selected_lab=LAB_TOPICS[0],
        selected_calc_type=CALCULATION_TYPES[0],
        selected_tutor_topic=TUTOR_TOPICS[0],
        selected_course=ENGINEERING_COURSES[0],
        show_steps_or_guide=True,
        latest_physics_output="Ready.",
        latest_calculus_output="Ready.",
        records=[],
    )

    p_idx: Page = index(test_state)
    assert_equal(p_idx.state.active_section, "Overview")

    p_phys: Page = physics(test_state)
    assert_equal(p_phys.state.active_section, "Physics Idea and Applications")

    p_s_phys: Page = solve_physics(
        test_state,
        "Lab 2: Inclined Plane Gravity",
        True,
        "0.052",
        "1.000",
        "0.505",
        "0.150",
    )
    assert_equal(len(p_s_phys.state.records), 1)
    assert_equal(p_s_phys.state.records[0].section, "Physics Idea and Applications")

    p_trials: Page = solve_trials(test_state, "5.2, 5.7, 5.5", "cm", "1")
    assert_equal(len(p_trials.state.records), 2)

    p_calc: Page = calculus(test_state)
    assert_equal(
        p_calc.state.active_section, "Calculus Calculations and Explanations"
    )

    p_s_calc: Page = solve_calculus(
        test_state,
        "Double Integral (∬ f(x,y) dx dy)",
        "x + y",
        "0, 1, 0, 2",
        True,
    )
    assert_equal(len(p_s_calc.state.records), 3)
    assert_equal(p_s_calc.state.records[2].final_yield, "3")

    p_exp: Page = explain_calculus(test_state, "Partial Derivatives")
    assert_equal(p_exp.state.selected_tutor_topic, "Partial Derivatives")

    p_app: Page = applications(test_state)
    assert_equal(
        p_app.state.active_section, "Engineering & Science Applications Info"
    )

    p_course: Page = select_engineering_course(test_state, "Fluid Mechanics")
    assert_equal(p_course.state.selected_course, "Fluid Mechanics")

    p_log: Page = log(test_state)
    assert_equal(p_log.state.active_section, "Combined Report Log")

    p_clr: Page = clear_log(test_state)
    assert_equal(len(p_clr.state.records), 0)


# Run all unit tests on startup before starting the web server
run_all_tests()

if __name__ == "__main__":
    # Note: start_server launches the live web server and blocks execution,
    # so it cannot be unit tested directly.
    start_server(
        State(
            active_section="Overview",
            selected_lab=LAB_TOPICS[0],
            selected_calc_type=CALCULATION_TYPES[0],
            selected_tutor_topic=TUTOR_TOPICS[0],
            selected_course=ENGINEERING_COURSES[0],
            show_steps_or_guide=True,
            latest_physics_output="Enter lab parameters above and click Solve.",
            latest_calculus_output="Choose a calculus type and click Calculate.",
            records=[],
        )
    )
