<script>
// import VueMarkdown from 'vue-markdown'
import { ref } from "vue";

const API_URL = "http://127.0.0.1:8000";
const ARTICLES_ENDPOINT = `${API_URL}/mongodb/articles`;
const ARTICLE_ENDPOINT = `${API_URL}/mongodb/article`;

async function get_article_ids() {
  const response = await fetch(ARTICLES_ENDPOINT);

  if (!response.ok) {
    const message = "An error has occured: ${response.status}";
    throw new Error(message);
  }

  const articles_json = await response.json();
  // console.log(articles_json);
  return articles_json;
}

async function get_one_article(article_id) {
  const response = await fetch(`${ARTICLE_ENDPOINT}/${article_id}`);

  if (!response.ok) {
    const message = "An error has occured: ${response.status}";
    throw new Error(message);
  }

  const article_json = await response.json();
  // console.log(article_json);
  return article_json;
}

async function get_articles(articles) {
  let article_ids = await get_article_ids();
  let article_contents = [];

  for (let article of article_ids["all_articles"]) {
    console.log(article["id"]);
    article_contents.push(get_one_article(article["id"]));
  }

  article_contents = await Promise.all(article_contents);
  console.log(article_contents);

  articles.value = article_contents;
}

export default {
  setup() {
    // components: {
    //   VueMarkdown: VueMarkdown;
    // }
    data: {
      let articles = ref([]);

      get_articles(articles);

      return { articles };
    }
  },
};
</script>

<template>
  <div id="articles">
    <div v-for="article of articles" :key="article['article']['date']">
      <p>{{ article["article"]["author"] }}</p>
      <p>{{ article["article"]["date"] }}</p>
      <p>{{ article["article"]["title"] }}</p>
      <p>{{ article["article"]["subtitle"] }}</p>
      <p>{{ article["article"]["cover"] }}</p>
      <div class="markdown">
        <vue-markdown>{{ article["article"]["content"] }}</vue-markdown>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
