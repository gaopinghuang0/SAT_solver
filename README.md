# SAT_solver
DPLL, GRASP, Chaff in Python2.7


## Directory structures
```
.
├── benchmarks
│   ├── VarNum1000-1500ClauseNum3000-8000
│   │   ├── random_v1087c7523.cnf
│   │   ├── ...
│   ├── VarNum100-1000ClauseNum1000-3000
│   │   ├── random_v242c2458.cnf
│   │   ├── ...
│   └── VarNum10-100ClauseNum100-1000
│       ├── random_v12c257.cnf
│       ├── ...
├── Chaff
│   ├── chaff.py
│   └── __init__.py
├── CHBR_glucose_agile
│   ├── bin
│   │   ├── CHBR_glucose
│   │   └── starexec_run_default
│   ├── code
│   │   ├── ...
├── DLL
│   ├── dll.py
│   └── __init__.py
├── GRASP
│   ├── grasp.py
│   └── __init__.py
├── __init__.py
├── mySolver.py
├── README.md
└── utils
    ├── data_types.py
    ├── dimacs_parser.py
    ├── file_generator.py
    ├── __init__.py
    ├── unittest_data_types.py
    └── utils.py
```

Explanation:
- benchmarks/ -- All the benchmark files are stored here and organized by their number of variables (i.e., VarNum10-100, VarNum100-1000, VarNum1000-1500)
- Chaff/chaff.py, GRASP/grasp.py, and DLL/dll.py -- Three solvers that we implemented
- CHBR_glucose_agile/ -- Gold standard solver, downloaded from [SAT competition 2016](http://baldur.iti.kit.edu/sat-competition-2016/solvers/agile/)
- mySolver.py -- excutable script
- utils/
  - data_types.py      -- Data structure for Literal and Clause
  - dimacs_parser.py   -- CNF file parser
  - file_generator.py  -- Generate random benchmarks
  - utils.py           -- memory_usage


## Compile code
Since it is written in Python, there is no need to compile code.
Gold standard solver is already compiled under CHBR_glucose_agile/bin/CHBR_glucose

mySolver.py and CHBR solver should already be excutable. If not, run the code below:
```
# make python script and CHBR solver excutable if they are not
chmod +x mySolver.py
chmod +x CHBR_glucose_agile/bin/CHBR_glucose
```

## Run
Tested on min server (min.ecn.purdue.edu)
```
mySolver.py benchmarks/**/*.cnf    # use Chaff by default
```

- Additional options:
```
-grasp        # use GRASP
-dll          # use DPLL, very slow
-time         # show runtime of solver
-mem          # show memory_usage, required to install "psutil", see below
-all          # solve all benchmarks
-all-vs-gold  # solve all benchmarks and compare results with CHBR solver
```

- How to install "psutil" on linux:
pip install --user psutil  (without root permission, install locally)
