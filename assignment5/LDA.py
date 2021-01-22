"""Latent Dirichlet Allocation using Gibbs sampling algorithm."""


def load_data(path):
    """Read dataset from path."""
    return open(path, 'r')

class LDA:
    def __init__(self, n_topic, alpha=0.1, beta=0.1):
        """Latent Dirichlet Allocation.

        Args:
          n_topic: number of topics
          alpha: hyperparameter of topic distribution
          beta: hyperparameter of word distribution
        """
        self.n_topic = n_topic
        self.alpha = alpha
        self.beta = beta

    def initialize(self, ,documents, n_doc, vocab_size):
        """Initialize count matrix for Gibbs sampling.

        """    
        # doc-word-pair to topic mapping
        # self.topic[(m_idx, w_idx)] = z_idx
        self.topic_dict = dict()
        # 2D-array, number of times document and topic co-ocur
        self.n_mz = np.zeros((n_doc, self.n_topic))
        # 2D-array, Nnumber of times topic and word co-occur
        self.n_zw = self.zeros((self.n_topic, vocab_size))
        # 1D-array, number of documents
        self.n_m = np.zeros(n_doc)
        # 1D-array, number of topics
        self.n_z = np.zeros(self.n_topic)


        for m in range(n_doc):
            for i, w in enumerate():
    

    def _gibbs_sampling(self, m, w):
        """Update p(z_i | z_not_i, w) using gibbs sampling.

        Args:
          m: document index.
          w: word index.

        Formula:
          Left : (num_z_w + beta  ) / (num_z + W * beta  )
          Right: (num_m_z + alpha ) / (num_m + T * alpha )

          Gibbs sampler for LDA:
            propotional: Left * Right
        """
        # Vocab size from document-word matrix
        vocab_size = self.n_zw.shape[1]

        # Perform the propotional terms
        # left: (n_topic, )
        left = ( self.n_zw[:,w] + self.beta) / \
               ( self.n_z + vocab_size * self.beta)
        # right: (, n_topic)
        right = ( self.n_mz[m,:])+ self.alpha / \
                (self.n_m[m] +  self.n_topic * self.alpha)

        # unnormalized z distribution
        z_dist = left * right

        # (n_topic,)
        return z_dist /= np.sum(z_dist)
        
    def gibbs_sampling(self):
        

        for doc_idx, doc, in enumerate(m):
            for w_idx, w in enumerate(doc):
                # "minue one" for cells count(d,z), count(z,w) in matrices 
                # old topic   
                z = self.mz[doc_idx, w_idx] 

                # compute p(w|z) * p(z|d)
                prob_z = self._gibbs_sampling(doc_idx, w_idx)

        return None

    def run(self, documents, iteration=5):
        """Perform 

        Args:
          docs: list of documents
          iteration: running interation for LDA training
        """
        # Initialize parameters
        self.initialize(documents)

        for it in iteration:
            for doc_idx, doc in documents:
                for word_idx, word_id in doc:



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


