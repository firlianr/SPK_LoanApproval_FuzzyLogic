import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --- Definisi Variabel Fuzzy ---
income = ctrl.Antecedent(np.arange(0, 25000, 1000), 'income')
loan = ctrl.Antecedent(np.arange(0, 700, 50), 'loan')
credit = ctrl.Antecedent(np.arange(0, 2, 1), 'credit')
approval = ctrl.Consequent(np.arange(0, 100, 1), 'approval')

# --- Fungsi Keanggotaan ---
income['low'] = fuzz.trimf(income.universe, [0, 0, 5000])
income['medium'] = fuzz.trimf(income.universe, [4000, 10000, 15000])
income['high'] = fuzz.trimf(income.universe, [12000, 20000, 25000])

loan['low'] = fuzz.trimf(loan.universe, [0, 0, 200])
loan['medium'] = fuzz.trimf(loan.universe, [150, 350, 500])
loan['high'] = fuzz.trimf(loan.universe, [450, 600, 700])

credit['poor'] = fuzz.trimf(credit.universe, [0, 0, 1])
credit['good'] = fuzz.trimf(credit.universe, [0, 1, 1])

approval['rejected'] = fuzz.trimf(approval.universe, [0, 0, 50])
approval['considered'] = fuzz.trimf(approval.universe, [25, 50, 75])
approval['approved'] = fuzz.trimf(approval.universe, [50, 100, 100])

# --- Aturan Fuzzy ---
rules = [
    ctrl.Rule(income['high'] & loan['low'] & credit['good'], approval['approved']),
    ctrl.Rule(income['high'] & loan['medium'] & credit['good'], approval['approved']),
    ctrl.Rule(income['high'] & loan['high'] & credit['good'], approval['considered']),
    ctrl.Rule(income['medium'] & loan['low'] & credit['good'], approval['approved']),
    ctrl.Rule(income['medium'] & loan['medium'] & credit['good'], approval['considered']),
    ctrl.Rule(income['medium'] & loan['high'] & credit['good'], approval['rejected']),
    ctrl.Rule(income['low'] & loan['low'] & credit['good'], approval['considered']),
    ctrl.Rule(income['low'] & (loan['medium'] | loan['high']), approval['rejected']),
    ctrl.Rule(income['high'] & credit['poor'], approval['considered']),
    ctrl.Rule((income['medium'] | income['low']) & credit['poor'], approval['rejected'])
]

# --- Sistem Fuzzy ---
approval_ctrl = ctrl.ControlSystem(rules)
approval_sim = ctrl.ControlSystemSimulation(approval_ctrl)


def predict_fuzzy(pendapatan, pinjaman, riwayat_kredit):
    """Fungsi untuk menghitung hasil fuzzy berdasarkan input pengguna"""
    credit_value = 1 if riwayat_kredit.lower() == "baik" else 0

    approval_sim.input['income'] = pendapatan
    approval_sim.input['loan'] = pinjaman
    approval_sim.input['credit'] = credit_value

    approval_sim.compute()
    return approval_sim.output['approval']
