"""Latent Dirichlet Allocation using Gibbs sampling algorithm."""

class LDA:
    def __init__(self):
        return None
    
    def __init__(self, n_topic, alpha=0.1, beta=0.1):
        """

        Args:
          n_topic: number of topics
          alpha: hyperparameter of topic distribution
          beta: hyperparameter of word distribution
        """
        self.n_topic = n_topic
        self.alpha = alpha
        self.beta = beta

    
    def _sample(self):
        return None



def run_lda():
    return None

def main():
    n_iteration = 2
    n_topic = 20
    model = LDA(n_topic=n_topic, alpha=0.02, beta=0.1)
    
    run_lda()

if __name__ == '__main__':
    main()


