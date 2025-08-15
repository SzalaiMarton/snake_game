import neural_network
import snake
import value

def main(episode):
    game = snake.Snake_Game()
    network = neural_network.MLP(12, [30, 30, 1])
    done = False

    for i in range(episode):
        c_reward = 0

        while not done:
            features = game.get_features()
            action = network(features)
            print(f"action: {action.data}")
            game.render(action.data)
            reward, done = game.evaluate_state()
            c_reward += reward

            loss = (action - reward)**2
            loss.backward() # not working as intended
            for p in network.parameters():
                p.data += -0.01 * p.grad

        game.reset()
        done = False
        print(f"Episode: {i}, Commulative reward: {c_reward}.")

    for p in network.parameters():
        p.data += -0.01 * p.grad
        print(p.data)

    
if __name__ == "__main__":
    main(1)