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

    def initialize(self, n_doc, vocab_size):
        """Initialize count matrix for Gibbs sampling.

        """
        
        # number of times document and topic co-ocur
        self.n_mz = self.zero((n_doc, self.n_topic))
        # number of times topic and word co-occur
        self.n_zw = self.zero((self.n_topic, vocab_size))
        # number of document
        self.n_m = np.zero(n_doc)
        # number of topic
        self.n_z = np.zero(self.n_topic)
    
        ###

    def _gibbs_sampling(self, m, w):
        """topic distribution.

            Left : (num_z_w + beta  ) / (num_z + W * beta  )
            Right: (num_m_z + alpha ) / (num_m + T * alpha )

        Gibbs sampler for LDA
            propotional: Left * Right
        """
        vocab_size = 0

        # Perform the propotional terms
        left = ( self.n_zw[:,w] + self.beta) / \
               ( self.n_z + vocab_size * self.beta)
        right = ( self.n_mz[m,:])+ self.alpha / \
                (self.n_m[m] +  self.n_topic * self.alpha)

        # unnormalized z distribution
        z_dist = left * right

        # (n_topic,)
        z_dist /= np.sum(z_dist)
        return z_dist
        
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


