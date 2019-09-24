
from src.utils.parse import *
from src.core.Simulation import *
from src.utils.plots import *

def run_simulation_all(rats_filename, lats_filename, setName=None):
    lats_fn = 'l' + rats_filename[1:]
    # static oracle
    oracle_timeouts = parseStaticOracleTimeouts(rats_filename + '_timeouts.csv')
    static_oracle_state = run_simulation(rats_filename + '.csv',lats_fn +'.csv', 'static', oracle_timeouts, 'STO')
    # #DSP
    dsp_timeouts = parseDSPTimeouts(rats_filename + '.csv', setName=setName)
    dsp_state = run_simulation(rats_filename + '.csv',lats_fn +'.csv', 'static', dsp_timeouts, 'DSP')
    # SPND
    spnd_timeouts = parseSPNDTimeouts(rats_filename +'.csv', lats_fn+'.csv', setName=setName)
    spnd_state = run_simulation(rats_filename + '.csv',lats_fn +'.csv', 'static', spnd_timeouts, 'SPND')
    # #Khronos
    constraintsToK = {0.1: 0, 0.2: 0.1, 0.3: 0.6, 0.4:1, 0.5:1.2, 0.6:1.4, 0.7:2, 0.8:2.8, 0.9:4.6, 1.0:280}
    khronos_state = run_simulation(rats_filename + '.csv',lats_fn +'.csv', 'ND_fixedK', constraintsToK, 'Khronos')
    #Oracle
    #oracle_constraints = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    #oracle_state = run_simulation(filename + '.csv', lats_fn + '.csv', 'oracle', oracle_constraints)
    #return [dsr_state.state, ndsr_state.state, static_oracle_state.state, khronos_state.state, oracle_state.state]
    return [dsp_state.state, spnd_state.state, static_oracle_state.state, khronos_state.state] #, oracle_state.state]

def run_simulation(rats_filename, lats_filename, approach, constraintsToK = None,timeouts=None, name=None):
    file = os.path.join(os.pardir, 'data_sets')
    # filename
    rats_filename = os.path.join(file, rats_filename)
    lats_filename = os.path.join(file, lats_filename)
    simulation = Simulation(rats_filename, lats_filename, 1, approach, constraintsToK = constraintsToK, timeouts=timeouts, name=name)
    simulation.initializeSimulation(rats_filename, lats_filename, approach)
    # if make_dist:
    #    createFolder(os.path.join(os.getcwd(), 'Distributions'))
    #    simulation.makeDistribution()
    simulation.runSimulation()
    simulation.analyzeSimulation()
    return simulation

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    constraintsToK = dict()
    for constraint in config['constraintsToK'].keys():
            constraintsToK[float(constraint)] = config['constraintsToK'][constraint]
    counter = 0
    while counter < len(config['rats_filenames']):
        result = run_simulation(config['rats_filenames'][counter], config['lats_filenames'][counter], 'fixedK', constraintsToK = constraintsToK)
        counter += 1
        print(result.state.__dict__['state']['1010/9000|fd34::0017:0d00:0030:dabe']['time_windows'][1.0]['mer'])
        print(result.state.__dict__['state']['1010/9000|fd34::0017:0d00:0030:dabe']['time_windows'][1.0]['pe'])
        print(result.state.__dict__['state']['1010/9000|fd34::0017:0d00:0030:dabe']['time_windows'][1.0]['prediction'])
        print(result.state.__dict__['state']['1010/9000|fd34::0017:0d00:0030:dabe']['relative_arrival_times'])
        makeTimePlot([result.state.state['1010/9000|fd34::0017:0d00:0030:dabe']['time_windows'][1.0]['prediction']], result.state.state['1010/9000|fd34::0017:0d00:0030:dabe']['relative_arrival_times'], ['Khronos'])