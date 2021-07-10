from PDDL import PDDL_Parser

class Planner:

    def heu(self, state, posgoals, neggoals):
        h = 0
        for i in posgoals:
            if i not in state:
                h += 1
        for i in neggoals:
            if i in state:
                h += 1
        return h

    #-----------------------------------------------
    # Solve
    #-----------------------------------------------

    def solve(self, domain, problem):
        # Parser
        parser = PDDL_Parser()
        parser.domainparser(domain)
        parser.problemparser(problem)
        # Parsed data
        state = parser.state
        posgoals = parser.positive_goals
        neggoals = parser.negative_goals
        # Do nothing
        if self.applicable(state, posgoals, neggoals):
            return []
        # Grounding process
        ground_actions = []
        for action in parser.actions:
            for act in action.groundify(parser.objects):
                ground_actions.append(act)
        # Search
        visited = [state]
        bounder = [state, None]
        while bounder:
            state = bounder.pop(0)
            plan = bounder.pop(0)
            h_min = 999
            for act in ground_actions:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    newstate = self.apply(state, act.add_effects, act.del_effects)
                    if newstate not in visited:
                        flag = 0
                        if self.heu(newstate, posgoals, neggoals) <= h_min:
                            flag = 1
                        if self.applicable(newstate, posgoals, neggoals):
                            full_plan = [act]
                            while plan:
                                act, plan = plan
                                full_plan.insert(0, act)
                            return full_plan
                        if flag == 1:
                            visited.append(newstate)
                            bounder.append(newstate)
                            bounder.append((act, plan))
        return None

    #-----------------------------------------------
    # Applicable
    #-----------------------------------------------

    def applicable(self, state, positive, negative):
        for i in positive:
            if i not in state:
                return False
        for i in negative:
            if i in state:
                return False
        return True

    #-----------------------------------------------
    # Apply
    #-----------------------------------------------

    def apply(self, state, positive, negative):
        newstate = []
        for i in state:
            if i not in negative:
                newstate.append(i)
        for i in positive:
            if i not in newstate:
              newstate.append(i)
        return newstate



# ==========================================
# Main
# ==========================================
if __name__ == '__main__':
    import sys, time
    start_time = time.time()
    domain = sys.argv[1]
    problem = sys.argv[2]
    planner = Planner()
    plan = planner.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    if plan:
        print('plan:')
        for act in plan:
            print(act)
    else:
        print('No plan was found!')