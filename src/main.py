'''
Created on 10.01.2022
This simulation shows that a fleeing spaceship has more time to defend itself from torpedos of a pursuing spaceship. It has a strategic advantage! (The Expanse Season 6 Episode 3: The Pella vs The Rocinante)
@author: Julian
'''


class Ship():

    def __init__(self, position, velocity, accleration, torpedo_acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = accleration
        self.torpedo_acceleration = torpedo_acceleration
    
    # update position and velocity
    def step(self, delta_t):
        self.position += delta_t * self.velocity
        self.velocity += delta_t * self.acceleration
        
    def fire(self, fire_foreward):
        if fire_foreward:
            torpedo_acceleration = self.torpedo_acceleration
        else:
            torpedo_acceleration = -self.torpedo_acceleration
        torpedo = Torpedo(self.position, self.velocity, torpedo_acceleration, fire_foreward)
        
        return torpedo

        
class Torpedo():

    def __init__(self, position, velocity, accleration, fired_foreward):
        self.position = position
        self.velocity = velocity
        self.acceleration = accleration
        self.fired_foreward = fired_foreward
        self.connected = None
        
    # update position and velocity
    def step(self, delta_t):
        self.position += delta_t * self.velocity
        self.velocity += delta_t * self.acceleration
       
    # check for collision between torpedo and enemy ship.
    def collision(self, ship, time):
        dif = ship.position - self.position
        collided = (dif >= 0 and not self.fired_foreward) or (dif <= 0 and self.fired_foreward)  # collision check
        if collided and (self.connected is None):  # register at what time the torpedo connected.
            self.connected = time
        return collided

    
def simulate():
    #===========================================================================
    # HERE YOU CAN PLAY WITH DIFFERENT SETTINGS TO OBSERVE THE OUTCOMES
    #===========================================================================
    delta_t = 0.001  # simulation precision
    free_navy_pella = Ship(position=0, velocity=900000000, accleration=50, torpedo_acceleration=1000)  # pella travelling at 900KM/s and accelerating with 5G. torpedo accelerate with 100G.
    torpedo_free_navy_pella = free_navy_pella.fire(True)  # Pella fires a torpedo at the Rocinante.
    rocinante = Ship(position=1000000, velocity=900000000, accleration=50, torpedo_acceleration=1000)  # rocinante is 1000KM away from the Pella (Railgun has around 1000KM max range), travelling at 900KM/s and accelerating with 5G. torpedo accelerate with 100G.
    torpedo_rocinante = rocinante.fire(False)  # Rocinante fires a torpedo at the Pella.
    
    # simulation loop
    step = 0
    while(True):
        # ship updates
        free_navy_pella.step(delta_t)
        rocinante.step(delta_t)
        # torpedo updates
        torpedo_free_navy_pella.step(delta_t)
        torpedo_rocinante.step(delta_t)
        # print(f"Distance between the Rocinante and the Pella:{int(rocinante.position-free_navy_pella.position + 0.5)}") # sanity check, should stay the same. uncomment to check.
        pella_hit = torpedo_rocinante.collision(free_navy_pella, step * delta_t)
        rocinante_hit = torpedo_free_navy_pella.collision(rocinante, step * delta_t)
        if pella_hit and rocinante_hit:
            break
        step += 1
    print(f"Torpedo from Rocinante connected after{torpedo_rocinante.connected: .2f} seconds with the Pella.")
    print(f"Torpedo from Pella connected after{torpedo_free_navy_pella.connected: .2f} seconds with the Rocinante.")
    print(f"This means, the Rocinante's PDCs have{100*(torpedo_free_navy_pella.connected/torpedo_rocinante.connected - 1): .2f}% more time to shoot down enemy torpedos.")

        
if __name__ == '__main__':
    simulate()
