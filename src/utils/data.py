"""Laman ng games galing sa Lesson 1-4 (Management and Organization Concepts).

MEMORY_PAIRS -> (term, short definition, lesson)
WORDS        -> (ANSWER, hint, lesson)
MANAGEMENT_SEQUENCE -> tamang pagkakasunod-sunod ng concepts para sa sliding puzzle
ROLE_DEPARTMENTS   -> listahan ng departamento para sa Team Role Matching
ROLE_TASKS         -> (task, tamang departamento, lesson)
"""

LESSON_NAMES = {
    1: "Lesson 1 - The Nature of Management",
    2: "Lesson 2 - Social Responsibility and Managerial Ethics",
    3: "Lesson 3 - International Management and Globalization",
    4: "Lesson 4 - Decision Making",
}

LESSON_CHOICES = {"Lahat ng Lesson (1-4)": None}
for _n, _name in LESSON_NAMES.items():
    LESSON_CHOICES[_name] = _n

# (term, short definition, lesson)
MEMORY_PAIRS = [
    # ---- Lesson 1 ----
    ("Management", "Process of assembling and using resources in a goal-directed manner", 1),
    ("Front-line Manager", "Lowest level; supervisors who train, motivate and monitor employees", 1),
    ("Middle Manager", "Turns top-level plans into specific objectives; tactical managers", 1),
    ("Top Manager", "Highest level (CEO, COO); sets overall direction; strategic managers", 1),
    ("Planning", "Estimating future conditions and deciding on courses of action", 1),
    ("Organizing", "Systematically integrating resources to accomplish tasks", 1),
    ("Directing", "Influencing other people to attain the organization's objectives", 1),
    ("Controlling", "Regulating the work of those a manager is responsible for", 1),
    ("Technical Skills", "Specialized knowledge of procedures, processes and equipment", 1),
    ("Interpersonal Skills", "Sensitivity, empathy and persuasiveness", 1),
    ("Conceptual Skills", "Reasoning, judgment and analytical thinking", 1),
    ("Decisional Skills", "Ability to make decisions or resolve problems", 1),
    ("Managing Change", "Start with \"small wins\" to build trust and acceptance", 1),
    # ---- Lesson 2 ----
    ("Ethics", "Study of right or wrong; a moral choice by an individual", 2),
    ("Ethical Dilemma", "Choice between two valid but conflicting options", 2),
    ("Ethical Lapse", "Decision made against stated values or policies", 2),
    ("Institutionalizing Ethics", "Applying and integrating ethical concepts with daily actions", 2),
    ("CSR", "Self-regulating business model for being socially accountable", 2),
    ("Economic Model", "Main goal of business: reasonable profit, quality goods and jobs", 2),
    ("Socio-economic Model", "Responsible to stockholders, employees, customers, suppliers, public", 2),
    ("Classical Model", "Use resources efficiently for profit within the rules of the game", 2),
    ("Environmental Responsibility", "Reducing pollution, recycling, replenishing natural resources", 2),
    ("Ethical Responsibility", "Fair treatment of customers, fair pay, transparency to investors", 2),
    ("Philanthropic Responsibility", "Donating profit to charities, sponsoring fundraising events", 2),
    ("Financial Responsibility", "Backing CSR plans with real investments in programs and R&D", 2),
    ("Golden Rule", "Governs management-employee relationship: treat others as you want to be treated", 2),
    ("Peter Drucker", "Management consultant: first responsibility to society is to operate at a profit", 2),
    # ---- Lesson 3 ----
    ("Internationalization", "Flow of goods, services, capital and knowledge across borders", 3),
    ("Globalization", "Integration and convergence of economic, financial, cultural and political systems", 3),
    ("Exporting", "Selling home-produced goods or services to foreign markets", 3),
    ("Licensing", "Granting a foreign company rights to produce or sell under your brand", 3),
    ("Joint Venture", "Companies from different countries share resources and risks", 3),
    ("Branch / Subsidiary", "Setting up local production and distribution facilities in the host country", 3),
    ("Managerial Services", "Offering expertise and management services to foreign businesses", 3),
    ("Global Supply Chain", "Integration of worldwide resources, markets and operations", 3),
    ("Outsourcing", "Tapping specialized skills abroad at lower cost", 3),
    ("Supply Chain Challenges", "Political instability, tariffs, disruptions, ethical concerns", 3),
    # ---- Lesson 4 ----
    ("Decision Making", "Choosing the best possible option from a range of alternatives", 4),
    ("Identify the Decision", "Step 1: define the nature of the decision to be made", 4),
    ("Gather Information", "Step 2: collect the relevant internal and external data", 4),
    ("Identify Alternatives", "Step 3: list the possible courses of action", 4),
    ("Weigh the Evidence", "Step 4: evaluate each alternative against the desired outcome", 4),
    ("Choose an Alternative", "Step 5: select the option that best fits the goal", 4),
    ("Take Action", "Step 6: implement the chosen alternative", 4),
    ("Review the Decision", "Step 7: evaluate the results and repeat the process if needed", 4),
    ("Individual Decision", "Faster, clear accountability; best in emergencies", 4),
    ("Group Decision", "Higher quality and creativity, stronger commitment, but slower", 4),
    ("Groupthink", "Desire for harmony overrides critique", 4),
    ("Group Polarization", "Groups move toward extreme positions", 4),
    ("Brainstorming", "Freely suggest ideas without immediate criticism", 4),
    ("Nominal Group Technique", "Write ideas independently, share in turn, then rank collectively", 4),
    ("Maslow's Hierarchy", "Participation satisfies belongingness, esteem and self-actualization", 4),
    ("Herzberg's Theory", "Hygiene factors prevent dissatisfaction; motivators drive performance", 4),
]

# (answer, hint, lesson)
WORDS = [
    # ---- Lesson 1 ----
    ("MANAGEMENT", "Process of assembling and using resources in a goal-directed manner", 1),
    ("PLANNING", "Function: estimating future conditions and deciding on courses of action", 1),
    ("ORGANIZING", "Function: systematically integrating resources to accomplish tasks", 1),
    ("DIRECTING", "Function: influencing people to attain the organization's objectives", 1),
    ("CONTROLLING", "Function: regulating the work of those a manager is responsible for", 1),
    ("SUPERVISORS", "Another name for front-line managers", 1),
    ("TACTICAL", "Middle managers are also called ____ managers", 1),
    ("STRATEGIC", "Top managers are also called ____ managers", 1),
    ("TECHNICAL", "Skill: specialized knowledge of procedures, processes and equipment", 1),
    ("INTERPERSONAL", "Skill: sensitivity, empathy and persuasiveness", 1),
    ("CONCEPTUAL", "Skill: reasoning, judgment and analytical thinking", 1),
    ("DECISIONAL", "Skill: ability to make decisions or resolve problems", 1),
    ("TECHNOLOGY", "Tool that improves efficiency and effectiveness in producing goods or services", 1),
    ("ENTREPRENEURIAL", "Managers must manage ____ly, always seeking and exploiting opportunities", 1),
    ("CHANGE", "Inevitable but often resisted; manage it with small wins", 1),
    ("MATERIALS", "The main inputs used to create goods and services", 1),
    # ---- Lesson 2 ----
    ("ETHICS", "The study of right or wrong", 2),
    ("DILEMMA", "A choice between two valid but conflicting options", 2),
    ("MORALITY", "Managerial ethics is rooted in this and business conduct", 2),
    ("STAKEHOLDERS", "Socio-economic model: responsibility to stockholders, employees, customers, etc.", 2),
    ("PHILANTHROPIC", "Type of CSR: donating profit to charities", 2),
    ("ENVIRONMENTAL", "Type of CSR: reducing pollution and recycling materials", 2),
    ("CLASSICAL", "Model followed by Milton Friedman", 2),
    ("ECONOMIC", "Model: society benefits most if business is left alone in its operations", 2),
    ("DRUCKER", "Peter ____, internationally famous management consultant", 2),
    ("CODE OF ETHICS", "Company policy that top managers establish to institutionalize ethics", 2),
    ("GOLDEN RULE", "Do unto others as you want others to do unto you", 2),
    ("CORPORATE CITIZENSHIP", "Another term for corporate social responsibility", 2),
    ("ETHICS COMMITTEE", "Formally appointed group used to institutionalize ethics", 2),
    # ---- Lesson 3 ----
    ("GLOBALIZATION", "Integration and convergence of economic, financial, cultural, political systems", 3),
    ("INTERNATIONALIZATION", "Flow of goods, services, capital and knowledge across country borders", 3),
    ("EXPORTING", "Selling goods or services produced at home to foreign markets", 3),
    ("LICENSING", "Granting a foreign company rights to produce or sell your products", 3),
    ("SUBSIDIARY", "Local facility set up in the host country (like Toyota's U.S. plants)", 3),
    ("JOINT VENTURE", "Partnership of companies from different countries (Jollibee & Viet Thai)", 3),
    ("SUPPLY CHAIN", "Globalization of this integrates worldwide resources, markets and operations", 3),
    ("OUTSOURCING", "Tech companies do this with software development to India", 3),
    ("TARIFFS", "Trade restriction that challenges global supply chains", 3),
    ("FOREIGN EXCHANGE", "International business earns this", 3),
    # ---- Lesson 4 ----
    ("DECISION", "Comes from \"decide\": to cut off or reach a conclusion", 4),
    ("BRAINSTORMING", "Freely suggesting ideas without immediate criticism", 4),
    ("NOMINAL GROUP TECHNIQUE", "Individuals write ideas independently, then share and rank them", 4),
    ("GROUPTHINK", "Desire for harmony overrides critique", 4),
    ("POLARIZATION", "Group ____: groups move toward extreme positions", 4),
    ("MASLOW", "Hierarchy of Needs theorist", 4),
    ("HERZBERG", "Motivation-Hygiene Theory theorist", 4),
    ("ALTERNATIVES", "Step 3 of the process: identify these", 4),
    ("EVALUATION", "Last step of decision making: review the outcome", 4),
    ("ACCOUNTABILITY", "Clear in individual decisions, shared in group decisions", 4),
    ("HYGIENE FACTORS", "Herzberg: factors that prevent dissatisfaction", 4),
    ("CONSENSUS", "Group decision-making sometimes needs this, which makes it slower", 4),
]


# Sliding Puzzle: Lesson 1 concepts in the order they are taught
# (levels of management from the top down, then the four functions).
MANAGEMENT_SEQUENCE = [
    "Management",
    "Top Manager",
    "Middle Manager",
    "Front-line Manager",
    "Planning",
    "Organizing",
    "Directing",
    "Controlling",
]


# Team Role Matching: mga departamento na puwedeng pagtalagahan ng gawain.
ROLE_DEPARTMENTS = [
    "Sales and Marketing",
    "Finance",
    "Operations",
    "Human Resources",
    "Information Technology",
]

# (task o empleyado, tamang departamento, lesson)
ROLE_TASKS = [
    # ---- Sales and Marketing ----
    ("Launch the advertising campaign for a new product line", "Sales and Marketing", 1),
    ("Handle customer inquiries and close deals with new clients", "Sales and Marketing", 1),
    ("Study competitors and survey what customers want to buy", "Sales and Marketing", 1),
    ("Set the monthly quota of the field sales representatives", "Sales and Marketing", 1),
    # ---- Finance ----
    ("Prepare the annual budget and the financial statements", "Finance", 1),
    ("Release payroll and pay the suppliers on time", "Finance", 1),
    ("Compute the taxes and file them with the government", "Finance", 1),
    ("Audit the cash flow before approving a big purchase", "Finance", 1),
    # ---- Operations ----
    ("Schedule the daily production of the factory", "Operations", 1),
    ("Check the quality of the finished goods before shipping", "Operations", 1),
    ("Monitor the inventory and reorder raw materials", "Operations", 1),
    ("Plan the delivery routes of the company trucks", "Operations", 1),
    # ---- Human Resources ----
    ("Recruit, interview and hire new employees", "Human Resources", 1),
    ("Run the training program for newly promoted supervisors", "Human Resources", 1),
    ("Handle employee grievances and disciplinary cases", "Human Resources", 1),
    ("Design the performance appraisal and benefits package", "Human Resources", 1),
    # ---- Information Technology ----
    ("Fix the company network and the employees' workstations", "Information Technology", 1),
    ("Back up the database and protect it from cyber attacks", "Information Technology", 1),
    ("Develop the online ordering system of the business", "Information Technology", 1),
    ("Install and update the software used by every department", "Information Technology", 1),
]


def filter_by_lesson(items, lesson):
    """Kunin lang ang items ng piniling lesson (None = lahat)."""
    if lesson is None:
        return list(items)
    return [it for it in items if it[2] == lesson]
