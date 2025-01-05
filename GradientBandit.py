import numpy as np
from scipy.special import softmax

class GradientBandit():
    def __init__(self,q_star_a,k=10,n_bandits=500,n_steps=500,alpha=0.1,with_reward_baseline=True):
        self.k = k
        self.n_bandits = n_bandits
        self.n_steps = n_steps
        self.alpha = alpha
        self.with_reward_baseline = with_reward_baseline


        self.q_star_a = q_star_a
        #print(self.q_star_a)
        self.H_t = np.array([0.0]*k)
        #print(self.H_t)
        self.reward_baseline = 0.0

    def select_action(self) -> int:
        selected_action = np.random.choice(range(self.k),p=softmax(self.H_t))
        return selected_action


    def get_reward(self,a):
        #1each reward for the action will come from the prob distribution of that action
        #which has a mean of q*(a) and variance of 1
        reward = np.random.normal(self.q_star_a[a],1) 
        return reward
    
    def calc_reward_baseline(self,step,reward):
        if step>0:
            self.reward_baseline = (self.reward_baseline*(step-1) + reward)/step
        else:
            self.reward_baseline = 0
        
    
    def update_numerical_preference(self,selected_action,reward):
        for action in range(self.k):
            if action == selected_action:
                self.H_t[selected_action] = self.H_t[selected_action] + self.alpha*(reward - self.reward_baseline)*(1-softmax(self.H_t)[selected_action])
            else:
                self.H_t[action] = self.H_t[action] - self.alpha*(reward - self.reward_baseline)*(softmax(self.H_t)[action])
        

    def one_step(self,step_num):
        selected_action = self.select_action()
        optimal_action = 0
        if selected_action == np.argmax(self.q_star_a) :
                optimal_action = 1
        reward = self.get_reward(selected_action)
        if self.with_reward_baseline:
            self.calc_reward_baseline(step_num,reward)
        else:
            self.reward_baseline = 0
        self.update_numerical_preference(selected_action,reward)
        return optimal_action

    def one_run(self):
        #self.reward_baseline = 0
        optimal_action_seq = []
        optimal_action_count = 0
        for step_num in range(1,self.n_steps+1):
            optimal_action = self.one_step(step_num)
            optimal_action_count += 1
            optimal_action_seq.append(optimal_action)
        return optimal_action_seq

    def run_bandit(self):
        o_a_runs = np.zeros((self.n_bandits,self.n_steps))

        for run in range(self.n_bandits):
            self.H_t = np.array([0.0]*self.k)
            o_a_runs[run] = self.one_run()
    
        #print(f"num bandits x num steps : {o_a_runs.shape}")
        optimal_action_perc = np.mean(o_a_runs,axis=0) * 100
        return optimal_action_perc