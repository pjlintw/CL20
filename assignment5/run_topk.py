
from pathlib import Path
import matplotlib.pyplot as plt

def load_k_word(w_word_file):
  topic_words = list()
  word_scores = list()
  with Path(w_word_file).open() as f:
    for line in f:
      word_buffer = list()
      score_buffer = list()
      # [('word', score), ('word', score), ...]
      for pair in line.strip().split(','):
        if pair == '':
          continue
        word, score = pair.split()
        word_buffer.append(word)
        score_buffer.append(int(float(score)))
      topic_words.append(word_buffer)
      word_scores.append(score_buffer)
  # 2D like lists
  return topic_words, word_scores
      

def plot_top_words(topic_words, word_scores, title):
    fig, axes = plt.subplots(4, 5, figsize=(30, 15), sharex=True)
    axes = axes.flatten()

    for topic_idx, topic in enumerate(topic_words):
        # top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        #top_features = [ str(ele) for ele in topic_words]
        # weights = topic[top_features_ind]
        # unnormalize logit (top_k, )
        #weights = topic[topic_idx]+ 1 

        ax = axes[topic_idx]
        ax.barh(topic, word_scores[topic_idx], height=0.7)
        ax.set_title(f'Topic {topic_idx +1}',
                     fontdict={'fontsize': 30})
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=20)
        for i in 'top right left'.split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.savefig('123.png')



if __name__ == '__main__':
  visual_path = Path('./results/2021-01-25_01-00-15/out.word')
  topic_words, word_scores = load_k_word(visual_path)
  plot_top_words(topic_words, word_scores, title='Topics in LDA')




