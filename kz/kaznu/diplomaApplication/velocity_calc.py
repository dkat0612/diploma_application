__author__ = 'dk@t'
import math


class Velocity:
    mu_water = 0.001
    delta_p = 1000.0
    l = 30000.0
    mu_oil = 0.025
    r = 0.5

    def __init__(self, r, mu_oil, delta_p, l):
        self.mu_oil = mu_oil
        self.r = r
        self.l = l
        self.delta_p = delta_p

    def __calculate_velocity(self, a, r):
        if r <= a:
            velocity = -(self.delta_p / (4 * self.l)) * ((r * r - a * a) / self.mu_oil + (a * a - self.r * self.r)
                                                         / self.mu_water)
        else:
            velocity = -(self.delta_p / (4 * self.l * self.mu_water)) * (r * r - self.r * self.r)
        return velocity

    def calculate_and_write(self):

        r = self.r
        eps = 0.001
        step = -0.001

        file = open("data/velocity.txt", "w", encoding='utf-8')
        header = "r[m],sigma_0.05,sigma_0.1,sigma_0.15,sigma_0.2,sigma_0.25\n"
        file.write(header)

        while r > eps:
            data = str(r)
            sigma = 0
            while math.fabs(sigma - 0.25) >= eps:
                sigma += 0.05
                a = self.r - sigma
                velocity = self.calculate_velocity(a, r)
                data += "," + str(velocity)
                data += "\n"
                file.write(data)
                r += step

            file.close()


if __name__ == "__main__":
    print("You need import this module to use")
    input("\n\nPress Enter to exit...")






