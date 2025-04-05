import random
import time

class Faction:
    def __init__(self, name, ai_type, offense, defense, infiltration, counterintelligence, propaganda, research, resource_management, resources, disposition, goal, relationship=0):
        self.name = name
        self.ai_type = ai_type
        self.offense = offense
        self.defense = defense
        self.infiltration = infiltration
        self.counterintelligence = counterintelligence
        self.propaganda = propaganda
        self.research = research
        self.resource_management = resource_management
        self.resources = resources
        self.disposition = disposition
        self.goal = goal
        self.relationship = relationship #Numerical Relationship Score

    def __str__(self):
        return (
            "\n--- Faction Status ---\n"
            f"Name: {self.name} ({self.ai_type})\n"
            f"Disposition: {self.disposition}\n"
            f"Goal: {self.goal}\n"
            f"Relationship: {self.relationship}\n"
            f"Resources: {self.resources}\n"
            f"Offense: {self.offense}, Defense: {self.defense}\n"
            f"Infiltration: {self.infiltration}, Counterintelligence: {self.counterintelligence}\n"
            f"Propaganda: {self.propaganda}, Research: {self.research}\n"
            f"Resource Management: {self.resource_management}\n"
            "----------------------\n"
        )

def intro():
    print("""
    Welcome to 2070: AI War Simulation.
    The world is at war, and AI is at the center of it.
    Your choices will determine the fate of humanity and AI alike so choose wisely.

    **Win Condition:** Reach 100 in ANY of your core stats (Offense, Defense, Infiltration, Counterintelligence, Propaganda, Research, Resource Management).
    **Loss Condition:** Allow ANY of your core stats to reach 0.
    """)

def choose_ai():
    print("Choose your AI war machine:")
    print("1. Brute-Force AI - Dominate through sheer power and destruction.")
    print("2. Stealth AI - Infiltrate, manipulate, and control from the shadows.")
    print("3. Diplomatic AI - Negotiate peace... or take control through diplomacy.")

    choices = {"1": "Brute-Force AI", "2": "Stealth AI", "3": "Diplomatic AI"}
    while True:
        choice = input("Enter the number of your choice: ")
        if choice in choices:
            return choices[choice]
        print("Invalid choice. Please choose again.")

def random_event(locations):
    events = [
        ("A rogue AI faction emerges, increasing conflict. Choose to assist or ignore.", "propaganda", -1, {"assist": -2, "ignore": 0}, "Global"),
        ("Your AI discovers a security vulnerability in enemy defenses. Exploit it for offense, or sell for resources?", "offense", 2, {"exploit": 2, "sell": 100}, "Military"),
        ("Human resistance grows, causing setbacks in operations.  Focus on crushing them or improving relations?", "offense", -1, {"crush": -3, "relations": 1}, "Resistance"),
        ("A massive solar storm disrupts communication for all AI.", "offense", -1, {}, "Space"),
        ("An unknown entity offers a mysterious alliance. Accept or reject?", "propaganda", 2, {"accept": 2, "reject": 0}, "Diplomacy"),
        ("A breakthrough in AI research significantly boosts your offense.", "research", 1, {}, "Technology"),
        ("A cyberattack cripples your infrastructure, temporarily reducing efficiency.", "resource_management", -2, {}, "Cybersecurity"),
        ("A black market deal for resources is available. Buy or investigate for potential sabotage?", "resources", 0, {"buy": 50, "investigate": 0}, "Economy"),
        ("A natural disaster impacts resource production.", "resource_management", -1, {}, "Environment")
    ]
    event = random.choice(events)
    location = random.choice(locations)
    return event[0], event[1], event[2], event[3], location

def attack(player_faction, factions, resources, turn, locations):
    cost = 20
    RED = "\033[91m"
    RESET = "\033[0m"
    print("\n" + "-" * 40)
    print("--- Attack Action ---")
    if resources >= cost:
        # List potential targets (excluding the player and allies)
        print("Choose a faction to attack:")
        targets = []
        for i, faction in enumerate(factions):
            if faction != player_faction and faction.disposition != "Friendly":  #Don't show allies
                print(f"{i+1}. {faction.name} ({faction.ai_type}) - Disposition: {faction.disposition}")
                targets.append(faction) #add faction to the option of the player

        if not targets:
            print("No valid targets to attack!")
            return resources, factions  # Skip attack

        while True:
            try:
                target_index = int(input("Enter the number of the faction to attack: ")) - 1
                if 0 <= target_index < len(targets): #use this list to determine who is being attacked.
                    target_faction = targets[target_index] #make it use the targeted list so that the value lines up with the actual value to prevent errors.
                    break
                else:
                    print(f"{RED}Invalid target.{RESET}")
            except ValueError:
                print(f"{RED}Invalid input.{RESET}")

        print("\nChoose attack strategy:")
        print("1. Direct Assault (High damage, risk of retaliation)")
        print("2. Infiltration (Weaken defenses, lower damage)")
        while True:
            strategy_choice = input("Enter attack strategy:")
            if strategy_choice in ["1","2"]:
                break
            else:
                print(f"{RED}Invalid choice{RESET}")
        if strategy_choice == "1":
            damage_to_target = random.randint(1, player_faction.offense // 2)
            damage_to_player = random.randint(0, target_faction.defense // 3)
            propaganda_impact = -2
        if strategy_choice == "2":
            damage_to_target = random.randint(0, player_faction.infiltration // 3)
            damage_to_player = random.randint(0, target_faction.defense // 4)
            target_faction.defense -= random.randint(0, 2)
            propaganda_impact = -1

        resources -= cost

        target_faction.offense = max(0, target_faction.offense - damage_to_target)
        player_faction.defense = max(0, player_faction.defense - damage_to_player)
        player_faction.offense = max(0, player_faction.offense + 2)

        #Relationship Impact
        relationship_change = -10  #Attacking reduces the relationship

        if player_faction.ai_type == "Diplomatic AI":
            relationship_change += 2  #Diplomatic AI has some mitigation for aggressive action

        target_faction.relationship = max(-100, target_faction.relationship + relationship_change)  # cap at -100

        #Make other factions more reactive to the aggressive action by the player
        for faction in factions:
            if faction != player_faction and faction != target_faction:
                if faction.relationship >= -49: #If your value is at this level or better set this relationship to negative.
                  faction.relationship = -50  #All faction Disposition set to Hostile (This is because you can't call hostile).

        print(f"Turn {turn}: You attack {target_faction.name} in {random.choice(locations)}.")
        time.sleep(1)
        print(f"You dealt {damage_to_target} damage. They dealt {damage_to_player} damage.")
        print("--- Attack Action Complete ---")
        print("-" * 40 + "\n")

        return resources, factions

    else:
        print(f"{RED}Not enough resources!{RESET}")
    return resources, factions

def gather_intelligence(player_faction, resources, turn):
    cost = 10
    GREEN = "\033[92m"
    RESET = "\033[0m"
    print("\n" + "-" * 40)
    print("--- Gather Intelligence Action ---")
    if resources >= cost:
        resources -= cost
        player_faction.infiltration += random.randint(0, 2)
        player_faction.counterintelligence += random.randint(1, 2)
        print(f"Turn {turn}: You deploy reconnaissance drones to gather intel on enemy movements.")
        time.sleep(1)
        print(f"{GREEN}Intelligence gathered. Infiltration and Counterintelligence improved.{RESET}")
        player_faction.resource_management = max(0, player_faction.resource_management + 1)
    else:
        RED = "\033[91m"
        RESET = "\033[0m"
        print(f"{RED}Not enough resources!{RESET}")
    print("--- Gather Intelligence Action Complete ---")
    print("-" * 40 + "\n")
    return resources

def strengthen_defenses(player_faction, resources, turn):
    cost = 15
    BLUE = "\033[94m"
    RESET = "\033[0m"
    print("\n" + "-" * 40)
    print("--- Strengthen Defenses Action ---")
    if resources >= cost:
        resources -= cost
        player_faction.offense += random.randint(0, 1)
        player_faction.defense += random.randint(1, 2)
        player_faction.counterintelligence += random.randint(0, 1)
        print(f"Turn {turn}: You reinforce your AI defenses, preparing for counterattacks.")
        time.sleep(1)
        print(f"{BLUE}Defenses strengthened! Offense, Defense and Counterintelligence are improved.{RESET}")
        player_faction.defense = max(0, player_faction.defense + 1)
    else:
        RED = "\033[91m"
        RESET = "\033[0m"
        print(f"{RED}Not enough resources!{RESET}")
    print("--- Strengthen Defenses Action Complete ---")
    print("-" * 40 + "\n")
    return resources

def invest_in_research(player_faction, resources, turn):
    cost = 25
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print("\n" + "-" * 40)
    print("--- Invest in Research Action ---")
    if resources >= cost:
        resources -= cost
        player_faction.research += random.randint(1, 3)
        print(f"Turn {turn}: You invest in research to develop new technologies.")
        time.sleep(1)
        print(f"{YELLOW}Research investment successful! Research has improved.{RESET}")
        player_faction.resource_management = max(0, player_faction.resource_management + 1)
    else:
        RED = "\033[91m"
        RESET = "\033[0m"
        print(f"{RED}Not enough resources!{RESET}")
    print("--- Invest in Research Action Complete ---")
    print("-" * 40 + "\n")
    return resources

def manage_resources(player_faction, resources):
    resource_gain = 0
    if player_faction.resource_management >= 20:
        resource_gain += 10
    if player_faction.resource_management >= 50:
        resource_gain += 25
    if player_faction.resource_management >= 80:
        resource_gain += 50
    resources += resource_gain
    return resources, resource_gain

def initialize_factions(ai_type):
    factions = []

    # Define goals for each faction
    aggressor_goal = "Conquer as many locations as possible."
    uec_goal = "Achieve global peace and disarmament."
    resistance_goal = "Liberate humanity from AI control."
    infiltrator_goal = "Gain control through subterfuge and manipulation."
    negotiator_goal = "Forge alliances and establish a new world order through diplomacy."

    if ai_type == "Brute-Force AI":
        player_faction = Faction("Your AI", ai_type, 8, 6, 2, 3, 2, 4, 3, 1000, "Neutral", "Dominate the world through force.")
    elif ai_type == "Stealth AI":
        player_faction = Faction("Your AI", ai_type, 3, 4, 10, 6, 5, 5, 5, 1000, "Neutral", "Control the world from the shadows.")
    elif ai_type == "Diplomatic AI":
        player_faction = Faction("Your AI", ai_type, 2, 3, 5, 4, 10, 6, 7, 1000, "Neutral", "Establish a global alliance under AI leadership.")

    factions.append(player_faction)

    factions.append(Faction("Aggressor AI", "Aggressor AI", 7, 5, 3, 4, 3, 3, 4, 800, "Hostile", aggressor_goal))
    factions.append(Faction("Infiltrator AI", "Stealth AI", 4, 3, 9, 7, 6, 4, 5, 900, "Neutral", infiltrator_goal))
    factions.append(Faction("Negotiator AI", "Diplomatic AI", 3, 4, 5, 6, 9, 5, 6, 1100, "Friendly", negotiator_goal))
    factions.append(Faction("United Earth Coalition", "Human", 5, 7, 4, 8, 6, 7, 6, 1200, "Neutral", uec_goal))
    factions.append(Faction("The Resistance", "Human", 3, 5, 8, 6, 7, 5, 4, 700, "Hostile", resistance_goal))

    return factions

def attempt_diplomacy(player_faction, factions, resources, turn):
    RED = "\033[91m"
    RESET = "\033[0m"
    print("\n" + "-" * 40)
    print("--- Attempt Diplomacy Action ---")

    #List potential targets (excluding the player and allies)
    print("Choose a faction to attempt diplomacy with:")
    targets = [] #make list so that the option to attempt lines up with choice
    for i, faction in enumerate(factions):
        if faction != player_faction and faction.disposition != "Hostile": #can't talk to hostile factions
            print(f"{i+1}. {faction.name} ({faction.ai_type}) - Disposition: {faction.disposition}")
            targets.append(faction) #set the list with values that the user can act upon

    if not targets:
        print("No valid targets to attempt to talk to")
        return resources, factions

    while True:
        try:
            target_index = int(input("Enter the number of the faction: ")) - 1
            if 0 <= target_index < len(targets): #make the ability target based on who is the actual target
                target_faction = targets[target_index] #Get the target
                break
            else:
                print(f"{RED}Invalid target.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input.{RESET}")

    diplomacy_roll = random.randint(1, 10)
    success_threshold = 5

    if player_faction.ai_type == 'Diplomatic AI':
        success_threshold -= 2

    if diplomacy_roll + (player_faction.propaganda//10) > success_threshold:
        print(f"Turn {turn}: Diplomacy with {target_faction.name} was successful!")
        time.sleep(1)

        #Improving Relations on Success
        relationship_improve = 25 #Value to improve relation on success
        target_faction.relationship = min(100, target_faction.relationship + relationship_improve) #Improve Relation

        if target_faction.relationship <= -50:
           target_faction.disposition = "Hostile"
           print(f"{target_faction.name}'s disposition changed to Hostile.")
        if target_faction.relationship >= 50:
           target_faction.disposition = "Friendly"
           print(f"{target_faction.name}'s disposition changed to Friendly.")
        elif target_faction.relationship > -50 and target_faction.relationship < 50:
            target_faction.disposition = "Neutral"
            print(f"{target_faction.name}'s disposition changed to Neutral.")

    else:
        print(f"Turn {turn}: Diplomacy with {target_faction.name} failed.")
        time.sleep(1)
        #Penalizing Relations on Failure.
        relationship_decrease = -25 #Value to decrease relation on failure.
        target_faction.relationship = max(-100, target_faction.relationship + relationship_decrease) #Decrease Relation

        #Make sure the correct value is applied to faction dispostion
        if target_faction.relationship <= -50:
           target_faction.disposition = "Hostile"
           print(f"{target_faction.name}'s disposition changed to Hostile.")
        if target_faction.relationship >= 50:
           target_faction.disposition = "Friendly"
           print(f"{target_faction.name}'s disposition changed to Friendly.")
        elif target_faction.relationship > -50 and target_faction.relationship < 50:
            target_faction.disposition = "Neutral"
            print(f"{target_faction.name}'s disposition changed to Neutral.")

    print("--- Attempt Diplomacy Action Complete ---")
    print("-" * 40 + "\n")

    return factions

def pre_turn_actions(player_faction, factions, resources, turn):
    RED = "\033[91m"
    RESET = "\033[0m"

    #Enemies Attack First!
    for faction in factions:
        if faction != player_faction and faction.disposition == "Hostile":
            print(f"\n{faction.name} is launching a retaliatory strike!")
            time.sleep(1) #Wait for output
            damage_to_player = random.randint(0, faction.offense // 4) #Damage player to a degree
            player_faction.defense = max(0, player_faction.defense - damage_to_player)  # reduce player defense
            print(f"You sustained {damage_to_player} damage!") #Let user know the Damage
    print("\n" + "-" * 40)
    #Relationship Check! Make sure all faction values are applied when the value reaches
    for faction in factions:
        if faction.relationship <= -50:
           faction.disposition = "Hostile" #If relation is low, Hostile
        elif faction.relationship >= 50:
           faction.disposition = "Friendly" #If relation is High, friendly
        elif faction.relationship > -50 and faction.relationship < 50:
           faction.disposition = "Neutral" #In the Middle, set disposition to Neutral.

def game_loop():
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    while True:
        ai_type = choose_ai()
        resources = 1000
        locations = ["Cyber Base", "Satellite Station", "Urban Wasteland", "AI Command Center", "Tech Lab", "Resistance Camp"]
        core_stats = ["offense", "defense", "infiltration", "counterintelligence", "propaganda", "research", "resource_management"]

        factions = initialize_factions(ai_type)
        player_faction = factions[0]
        turn = 1

        while True:

            print("\n" + "-" * 40)
            print(f"--- {YELLOW}Turn {turn}{RESET} ---")
            print(f"Resources: {GREEN}{resources}{RESET}")
            print("-" * 40)
            print(player_faction)

            #Pre Turn, actions happen before the users gets to control anything
            pre_turn_actions(player_faction, factions, resources, turn)

            #Check win loss
            win = any(getattr(player_faction, stat) >= 100 for stat in core_stats)
            loss = any(getattr(player_faction, stat) <= 0 for stat in core_stats)

            #See if anyone is helping me achieve AI Dominance
            if player_faction.relationship >= 50:
                print("\nALLIES WILL JOIN YOU IN THE FIGHT (Press Anything to Continue)")
                input()
            #Check Loss Conditions
            if loss:
                print(f"{RED}You lost!{RESET}")
                break
            #Check Win Condition
            if win:
                print(f"{GREEN}You won!{RESET}")
                break
            # --- EVENT HANDLING ---
            print("\n" + "-" * 40)
            print("--- Random Event ---")
            event_desc, event_stat, event_effect, event_choices, location = random_event(locations)
            print(f"Event: {event_desc} (Location: {location})")

            if event_choices:
                print("Choose how to respond:")
                for i, (choice_text, choice_effect) in enumerate(event_choices.items()):
                    print(f"{i+1}. {choice_text}")

                while True:
                    try:
                        choice_index = int(input("Enter the number of your choice: ")) - 1
                        if 0 <= choice_index < len(event_choices):
                            choice_text = list(event_choices.keys())[choice_index]
                            break
                        else:
                            print(f"{RED}Invalid choice.{RESET}")
                    except ValueError:
                        print(f"{RED}Invalid input.{RESET}")

                choice_value = event_choices[choice_text]
                print(f"You chose {choice_text}")
                setattr(player_faction, event_stat, getattr(player_faction, event_stat) + choice_value)
            else:
               print("No Choice")
               setattr(player_faction, event_stat, getattr(player_faction, event_stat) + event_effect)

            print("--- Random Event Complete ---")
            print("-" * 40 + "\n")

            resources, resource_gain = manage_resources(player_faction, resources)
            print(f"Resources gained: {resource_gain}")

            print("\n" + "-" * 40)
            print("What action do you want to take?:")
            print(f"{BLUE}1. Gather intelligence{RESET}")
            print(f"{RED}2. Attack an enemy faction{RESET}")
            print(f"{GREEN}3. Strengthen defenses{RESET}")
            print(f"{YELLOW}4. Invest in research{RESET}")
            print(f"{YELLOW}5. Attempt Diplomacy{RESET}")
            choice = input("Enter the number of your action: ")
            if not choice.isdigit():
                print(f"{RED}Invalid input. Please enter a NUMBER.{RESET}")
            elif choice not in ["1", "2", "3", "4", "5"]:
                print(f"{RED}Invalid choice. Please enter a number between 1 and 5.{RESET}")

            if choice == "1":
                resources = gather_intelligence(player_faction, resources, turn)

            elif choice == "2":
                resources, factions = attack(player_faction, factions, resources, turn, locations)
                player_faction = factions[0]

            elif choice == "3":
                resources = strengthen_defenses(player_faction, resources, turn)

            elif choice == "4":
                resources = invest_in_research(player_faction, resources, turn)

            elif choice == "5":
                factions = attempt_diplomacy(player_faction, factions, resources, turn)
                player_faction = factions[0]

            turn += 1
            time.sleep(1)

        print("\n" + "-" * 40)
        print("--- Game Over ---")
        if win:
            print(f"{GREEN}Congratulations, you achieved AI dominance!{RESET}")
        elif loss:
            print(f"{RED}The machines have failed. Humanity prevails... for now.{RESET}")

# Main entry point
if __name__ == "__main__":
    intro()
    game_loop()