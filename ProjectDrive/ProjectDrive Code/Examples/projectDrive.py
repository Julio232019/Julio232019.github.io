from textx import metamodel_from_file

# Car class definition
class Car:
    def __init__(self, name, model, color, max_speed, fuel, engine_status):
        self.name = name
        self.model = model
        self.color = color
        self.max_speed = max_speed
        self.fuel = fuel
        self.engine_status = engine_status
        self.speed = 0

    def __str__(self):
        return f"{self.name} - {self.model}, Speed: {self.speed} mph, Fuel: {self.fuel}%"

    def accelerate(self, amount):
        if self.engine_status == "Off":
            print(f"{self.name}'s engine is turned off. You need to turn it on to drive!")
        else:
            if amount + self.speed > self.max_speed:
                print(f"{self.name} cannot accelerate past {self.max_speed} mph!")
            else:

                if self.fuel > 0:
                    self.speed += amount
                    self.fuel -= amount * 0.1
                    print(f"{self.name} accelerates by {amount} mph. Current speed: {self.speed} mph.")

                else:
                    print(f"{self.name} is out of fuel!")
                    quit()

    def drive(self, direction, distance):
        if self.engine_status == "Off":
            print(f"{self.name}'s engine is turned off. You need to turn it on to drive!")
        else:
            if self.fuel > 0:
                self.speed = 50
                self.fuel -= distance * 0.05
                print(f"{self.name} is driving {direction} for {distance} miles at {self.speed} mph.")
            else:
                print(f"{self.name} is out of fuel!")
                quit()

    def turn(self, direction, degrees):
        print(f"{self.name} turned {direction} by {degrees} degrees.")

    def brake(self, amount):

        if self.speed == 0:
            print(f"{self.name} is already stopped.")
        elif amount >= self.speed:
            self.speed = 0
            print(f"{self.name} has come to a stop")
        elif self.speed > 0:
            self.speed = max(0, self.speed - amount)
            print(f"{self.name} slows down by {amount} mph. Current speed: {self.speed} mph.")
        else:
            print(f"{self.name} is already stopped.")

    def stop(self):
        if self.speed == 0:
            print(f"{self.name} is already stopped.")
        else:
            self.speed = 0
            print(f"{self.name} has stopped.")

    def check_status(self, status_type):
        if status_type == "fuel":
            print(f"{self.name}'s fuel: {self.fuel}%")
        elif status_type == "speed":
            print(f"{self.name}'s speed: {self.speed} mph")
        elif status_type == "engine_status":
            print(f"{self.name}'s engine status: {self.engine_status}")
    def turnOn(self):
        if self.engine_status == "Off":

            self.engine_status = "On"
            print(f"{self.name}'s engine has turned on!")
        else:
            print(f"{self.name}'s engine is already on!")


#Interpret Function
def interpret(model):
    cars = {}

    for c in model.commands:
        if c.__class__.__name__ == "CarDefinition":
            
            car = Car(
                c.name,
                c.model,
                c.color,
                c.max_speed,
                c.fuel,
                c.engine_status
            )
            cars[c.name] = car
            print(f"Created car: {car}")

        elif c.__class__.__name__ == "MoveCommand":
            car = cars.get(c.car)
            if car:
                if c.direction == "forward":
                    car.drive('forward', c.distance)
                elif c.direction == "backward":
                    car.drive('backward', c.distance)
                elif c.direction == "left":
                    car.turn('left', c.distance)
                elif c.direction == "right":
                    car.turn('right', c.distance)
            else:
                print(f"Car '{c.car}' not found!")

        elif c.__class__.__name__ == "AccelerateCommand":
            car = cars.get(c.car)
            if car:
                car.accelerate(c.amount)
            else:
                print(f"Car '{c.car}' not found!")

        elif c.__class__.__name__ == "CheckStatusCommand":
            car = cars.get(c.car)
            if car:
                car.check_status(c.status_type)
            else:
                print(f"Car '{c.car}' not found!")

        elif c.__class__.__name__ == "StopCommand":
            car = cars.get(c.car)
            if car:
                car.stop()
            else:
                print(f"Car '{c.car}' not found!")

        elif c.__class__.__name__ == "BrakeCommand":
            car = cars.get(c.car)
            car.brake(c.amount)
        elif c.__class__.__name__ == "EngineCommand":
            car = cars.get(c.car)
            car.turnOn();

        else:
            print(f"Unknown command: {c.__class__.__name__}")


car_mm = metamodel_from_file('ProjectDrive.tx')


car_model = car_mm.model_from_file('example2.drive')


interpret(car_model)
