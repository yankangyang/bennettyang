    possible = util.Counter();
    for p in self.legalPositions:
        nextState = self.setGhostPosition(gameState,p);
        model = self.getPositionDistribution(gameState);
        for newpos in model.sortedKeys():
            possible[newpos] = self.beliefs[p] * model[newpos];
    
    self.beliefs = possible;
  def getBeliefDistribution(self):
    return self.beliefs



    