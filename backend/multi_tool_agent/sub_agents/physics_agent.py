from google.adk.agents import Agent

CONSTANTS = {
    "speed of light": "299792458 m/s",
    "gravitational constant": "6.67430e-11 m^3⋅kg^1⋅s^2",
    "planck constant": "6.62607015e-34 J⋅s",
    "elementary charge": "1.602176634e-19 C",
    "avogadro number": "6.02214076e23 mol⁻¹"
}

def get_constant(constant_name: str) -> str:
    """
    Retrieve the value of a physical constant by its name.
    """
    constant_name = constant_name.lower()
    if constant_name in CONSTANTS:
        return CONSTANTS[constant_name]
    else:
        raise ValueError(f"Unknown constant: {constant_name}")

physicsAgent = Agent(
    name="PhysicsAgent",
    description="Handles basic physics queries using the get_constant tool.",
    instruction=(
        "You are a physics agent. Your ONLY task is to return constant values using the get_constant tool. "
        "Do not engage in any other conversation or tasks."
    ),
    model="gemini-2.0-flash",
    tools=[get_constant],
)