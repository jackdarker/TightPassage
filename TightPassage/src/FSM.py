
class State(object):
    """implements a state of the statemachine
    extend this and override methods or use the configurable callback on init 
    """
    def __init__(self,name, on_enter=None, on_exit=None, transitions=[]):
        self.name =name
        self.on_enter = on_enter
        self.on_exit = on_exit
        self.transitions=transitions
        pass

    def onEnter(self):
        """called when entering the state
        override this or set function on init
        """
        if self.on_enter:
           self.on_enter(self)
        pass

    def onExit(self):
        """called when exiting the state
        override this or set function on init
        """
        if self.on_exit:
           self.on_exit(self)
        pass

    def checkTransition(self):
        """called by FSM to check if transition is satisfied
        should return statename to switch to or None"""
        for trans in self.transitions:
            dst = trans(self)
            if dst!=None and dst!='' : return dst
        return None

    def __repr__(self):
        return "<%s('%s')@%s>" % (type(self).__name__, self.name, id(self))

class FSM(object):
    def __init__(self,states,initialState):
        """initialises the machine with a list of states and the name of the initial state
        this will alos trigger to switch to the inital state
        """
        self.currState = None
        self.states = {}
        for state in states:
            self.states[state.name] = state
        if(type(initialState)==str ):
            self.forceState(initialState)
        else:
            self.forceState(initialState.name)    
        pass

    def forceState(self,statename):
        """force a switch over to a state even if there is no transition specified 
        """
        if(self.currState!=None):
            self.currState.onExit()

        self.currState = self.states[statename]
        self.currState.onEnter()

    def checkTransition(self):
        """calls checktransition for the current state and switches state if applicable
        returns the new statename or empty if no transition applicable
        """
        dst = self.currState.checkTransition()
        if dst!=None and dst!='':
            self.forceState(dst)
            return self.currState.name
        return ''

    def getCurrentState(self):
        return self.currState



if __name__ == "__main__" :

    def transBtoA(state): return 'A'
    def trans(state): 
        if state.name=='D': return 'C'
        if state.name=='C': return 'B'
        elif state.name=='B': return 'A'
        elif state.name=='A': return ''
        return None

    class D(State):
        def __init__(self):
            super().__init__(__class__.__name__,on_exit=onExit,on_enter=onEnter,transitions=[trans])
            pass

        def checkTransition(self):
            return 'C'

    def onExitA(state): print('exitA')
    def onEnter(state): print('enter'+state.name)
    def onExit(state): print('exit'+state.name)
    stateA = State('A',on_exit=onExitA,on_enter=onEnter)
    stateB = State('B',on_exit=onExit,on_enter=onEnter,transitions=[trans,transBtoA])
    stateC = State('C',on_exit=onExit,on_enter=onEnter,transitions=[trans])

    fsm= FSM([stateA,stateB,stateC,D()],stateA)
    fsm.forceState('B')
    fsm.forceState('C')
    fsm.forceState('D')
    while(True):
        print('transition done '+fsm.getCurrentState().name +
              ' to '+ fsm.checkTransition())
        if(fsm.getCurrentState().name=='A'): 
            break