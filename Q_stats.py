import numpy as np




def main():
    Q_table = np.load('/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/Q_table.npy')
    actions = np.load("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/actions.npy")
    sates = np.load("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/states.npy")
    print(Q_table.shape)

    count = 0
    for i in range(Q_table.shape[0]):
        num_non_zero = np.count_nonzero(Q_table[i])
        total = (Q_table[i]).size
        if num_non_zero != 0 and sum(Q_table[i]) > 0:

            print(f"state {i}: {num_non_zero}/{total} entries filled (optimal action: {actions[np.argmax(Q_table[i])]}")
        else:
            count += 1
            #print(f"state {i}: {num_non_zero}/{total} entries filled (no optimal action)")

    print(f"number of states not visited/no positive Q-value: {count}")




if __name__ == "__main__":
    main()
