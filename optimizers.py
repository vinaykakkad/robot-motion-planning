import time
import mdptoolbox
import numpy as np


def fit_policy(st, rm, gamma, num_states):
    """
    This function trains an optimal policy using Markov Decision Process
    using MDPToolbox using PolicyIteration

    """
    iterations = list(range(1, 1000, 10))
    data_policy = {}
    data_policy["convergence"] = {}

    for iter in iterations:

        print("Current Iteration: {}".format(iter))

        data_policy[str(iter)] = {}

        tot_time_start = time.time()
        vi = mdptoolbox.mdp.PolicyIteration(
            st, rm, gamma, max_iter=10000000, eval_type=1
        )
        # vi.setVerbose()
        time_iter, iter_value, iter_policy, policy_change, policies = vi.run(
            max_iter=iter
        )
        tot_time_end = time.time()
        tot_time = tot_time_end - tot_time_start

        policy_change = [int(x) for x in policy_change]
        if np.any(np.array(iter_value) > iter):
            raise ValueError(
                "Value loop of Policy Iteration not stopping at maximum iterations provided"
            )

        data_policy[str(iter)]["tot_time"] = tot_time
        data_policy[str(iter)]["time_iter"] = time_iter
        data_policy[str(iter)]["policy_iter"] = iter_policy
        data_policy[str(iter)]["value_iter"] = iter_value
        data_policy[str(iter)]["policy_change"] = policy_change

    print("Convergence")
    tot_time_start = time.time()
    vi = mdptoolbox.mdp.PolicyIteration(
        st, rm, gamma, max_iter=10000000, eval_type=1
    )
    time_iter, iter_value, iter_policy_policy, policy_change, policies = vi.run(
        max_iter=10000
    )
    tot_time_end = time.time()

    policy_change = [int(x) for x in policy_change]
    policies = [tuple(int(x) for x in opt_policy) for opt_policy in policies]
    optimal_policy = vi.policy
    expected_values = vi.V
    optimal_policy = tuple(int(x) for x in optimal_policy)
    expected_values = tuple(float(x) for x in expected_values)

    optimal_policy = dict(zip(list(range(num_states)), list(optimal_policy)))
    expected_values = list(expected_values)
    policies = [
        dict(zip(list(range(num_states)), list(opt_policy)))
        for opt_policy in policies
    ]

    data_policy["convergence"]["tot_time"] = tot_time_end - tot_time_start
    data_policy["convergence"]["time_iter"] = time_iter
    data_policy["convergence"]["policy_iter"] = iter_policy_policy
    data_policy["convergence"]["value_iter"] = iter_value
    data_policy["convergence"]["policy_change"] = policy_change
    data_policy["convergence"]["optimal_policy"] = optimal_policy
    data_policy["convergence"]["expected_values"] = expected_values
    data_policy["convergence"]["policies"] = policies

    return data_policy


def fit_value(st, rm, gamma, num_states):
    """
    This function trains an optimal policy using Markov Decision Process using MDPToolbox
    using ValueIteration

    """
    iterations = list(range(1, 1000, 10))
    data_value = {}
    data_value["convergence"] = {}
    for iter in iterations:

        print("Current Iteration: {}".format(iter))
        data_value[str(iter)] = {}

        tot_time_start = time.time()
        vi = mdptoolbox.mdp.ValueIteration(
            st, rm, gamma, max_iter=10000000, epsilon=0.0001
        )
        # vi.setVerbose()
        time_iter, iter_value, variation, policies = vi.run(max_iter=iter)
        tot_time_end = time.time()
        tot_time = tot_time_end - tot_time_start

        if iter_value > iter:
            raise ValueError(
                "ValueIteration is not stopping at maximum iterations"
            )

        data_value[str(iter)]["tot_time"] = tot_time
        data_value[str(iter)]["time_iter"] = time_iter
        data_value[str(iter)]["value_iter"] = iter_value
        data_value[str(iter)]["variation"] = variation

    print("Convergence")
    tot_time_start = time.time()
    vi = mdptoolbox.mdp.ValueIteration(
        st, rm, gamma, max_iter=10000, epsilon=0.0001
    )
    time_iter, iter_value, variation, policies = vi.run(max_iter=10000)
    tot_time_end = time.time()

    optimal_policy = vi.policy
    expected_values = vi.V
    policies = [tuple(int(x) for x in opt_policy) for opt_policy in policies]
    optimal_policy = tuple(int(x) for x in optimal_policy)
    expected_values = tuple(float(x) for x in expected_values)

    optimal_policy = dict(zip(list(range(num_states)), list(optimal_policy)))
    expected_values = list(expected_values)
    policies = [
        dict(zip(list(range(num_states)), list(opt_policy)))
        for opt_policy in policies
    ]

    data_value["convergence"]["tot_time"] = tot_time_end - tot_time_start
    data_value["convergence"]["time_iter"] = time_iter
    data_value["convergence"]["value_iter"] = iter_value
    data_value["convergence"]["variation"] = variation
    data_value["convergence"]["optimal_policy"] = optimal_policy
    data_value["convergence"]["expected_values"] = expected_values
    data_value["convergence"]["policies"] = policies

    return data_value
