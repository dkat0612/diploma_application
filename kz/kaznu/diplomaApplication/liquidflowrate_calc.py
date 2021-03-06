__author__ = 'dk@t'
import math


class LiquidFlowRate:
    mu_water = 0.001
    delta_p = 1000.0
    l = 30000.0
    mu_oil = 0.025
    sigma = 0
    step = 0.001
    r = 0.5

    def __init__(self, r, mu_oil, delta_p, l):
        self.delta_p = delta_p
        self.r = r
        self.mu_oil = mu_oil
        self.l = l

    def q_water(self, a):
        return -(math.pi / (8 * self.mu_water)) * (-self.delta_p / self.l) * math.pow(math.pow(self.r, 2.0)
                                                                                      - math.pow(a, 2.0), 2.0)

    def q_oil(self, a):
        return -(math.pi / 4) * (-self.delta_p / self.l) * (math.pow(a, 4.0) / (2 * self.mu_oil) - math.pow(a, 4.0) /
                                                            self.mu_water + (math.pow(self.r, 2.0) *
                                                                             math.pow(a, 2.0)) / self.mu_water)

    def q(self):
        mu_pseudo_water = 0.025
        return (math.pi / (8 * mu_pseudo_water)) * (self.delta_p / self.l) * math.pow(self.r, 4.0)

    def calculate_and_write(self):
        q_pure_oil = self.q()
        sigma = 0
        step = 0.001

        file = open("data/liquidflowrate.csv", "w", encoding='utf-8')
        header = "sigma,q,q_water,q_oil\n"
        file.write(header)

        while sigma < self.r:
            a = self.r - sigma
            q_w = self.q_water(a)
            q_o = self.q_oil(a)
            sigma += step
            data = str(sigma) + "," + str(q_pure_oil) + "," + str(q_w) + "," + str(q_o) + "\n"
            file.write(data)

        file.close()

        # optimal value of a
        a = self.r / math.pow(2.0 - self.mu_water / self.mu_oil, 0.5)
        q_w = self.q_water(a)
        q_o = self.q_oil(a)

        file = open("data/optimal_values.csv", "w", encoding='utf-8')
        x = str(self.r - a) + "," + str(self.r - a) + "," + str(self.r - a)+"\n"
        y = str(q_pure_oil) + "," + str(q_w) + "," + str(q_o)+"\n"
        file.write(x)
        file.write(y)
        file.close()


if __name__ == '__main__':
    print("You need import this module to use")
    input("\n\nPress Enter to exit...")



