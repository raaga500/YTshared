from GradientBandit import GradientBandit
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,10)
import numpy as np
import time
import concurrent.futures

#EXPERIMENT
N_BANDITS = 2000
N_STEPS = 1000
ALPHA = [0.05,0.1,0.4]

TRUE_REWARD_MEAN = 0.0
TRUE_REWARD_VAR = 1.0

# N_BANDITS = 500
# N_STEPS = 500
# ALPHA = [0.05]

def run_bandit_in_parallel(q_star_a, k, n_bandits, n_steps, alpha, with_reward_baseline):
    bandit = GradientBandit(q_star_a, k, n_bandits, n_steps, alpha, with_reward_baseline)
    return bandit.run_bandit()


def run_experiment(k=10,n_bandits=500,n_steps=500,alpha=[0.05,0.1,0.4]):
    optimal_action_perc_dict = {}
    q_star_a = np.random.normal(TRUE_REWARD_MEAN,TRUE_REWARD_VAR,k) #sample for mean 0 distribution instead of +4
    print(f"True Q values: {q_star_a}")

    #collect all tasks for parallel execution
    tasks = [] 

    #collect all tasks for parallel execution
    future_to_key={}

    with concurrent.futures.ProcessPoolExecutor() as executor:

        for bandit_n,alpha_value in enumerate(alpha):
            future_wrb_T = executor.submit(run_bandit_in_parallel, q_star_a, k, n_bandits, n_steps, alpha[bandit_n], True)
            key_wrb_T = f"Gradient bandit with alpha={alpha_value} with Reward Baseline"
            future_to_key[future_wrb_T] = key_wrb_T
            print(f"Submitted {key_wrb_T} for execution")

            future_wrb_F = executor.submit(run_bandit_in_parallel, q_star_a, k, n_bandits, n_steps, alpha[bandit_n], False)
            key_wrb_F = f"Gradient bandit with alpha={alpha_value} without Reward Baseline"
            future_to_key[future_wrb_F] = key_wrb_F
            print(f"Submitted {key_wrb_F} for execution")

            
        for future in  concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                optimal_action_perc_dict[key] = future.result()
            except Exception as e:
                print(f"Error occurred for key {key}: {e}")        
        
    return optimal_action_perc_dict

# start_time = time.perf_counter()
# optimal_action_perc_dict = run_experiment(n_bandits=N_BANDITS,n_steps=N_STEPS,alpha=ALPHA)
# end_time = time.perf_counter()


if __name__ == "__main__":
    start_time = time.perf_counter()
    optimal_action_perc_dict = run_experiment(n_bandits=N_BANDITS, n_steps=N_STEPS, alpha=ALPHA)
    end_time = time.perf_counter()
    #print(optimal_action_perc_dict)

    print(f"Execution time: {end_time - start_time:.6f} seconds")

    #Plot
    for experiment_result_key in optimal_action_perc_dict.keys():
        print(experiment_result_key)
        data = optimal_action_perc_dict[experiment_result_key]
        plt.plot(data,label=experiment_result_key);
        plt.ylabel("% Optimal Action")
        plt.xlabel("Steps")

    handles, labels = plt.gca().get_legend_handles_labels()
   # Sort the labels and their corresponding handles alphabetically
    sorted_handles_labels = sorted(zip(labels, handles), key=lambda x: x[0])
    sorted_labels, sorted_handles = zip(*sorted_handles_labels)  
    plt.legend(sorted_handles,sorted_labels);

    #plt.show()

    plt.savefig("GradientBandit_Run.svg", format='svg', dpi=300)
    plt.close()  # Close the plot to free memory

    print('Plot saved to disk')


