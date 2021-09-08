<script>
// import VueMarkdown from 'vue-markdown'
import { ref } from "vue"

const API_URL = "http://127.0.0.1:8000"
const ARTICLES_ENDPOINT = `${API_URL}/mongodb/articles`

async function get_articles(url, articles) {
  const response = await fetch(url);

  if (!response.ok) {
    const message = "An error has occured: ${response.status}";
    throw new Error(message);
  }

  const articles_json = await response.json();
  console.log(articles_json);
  articles.value = articles_json;
}

export default {
  setup() {
    let articles = ref([]);

    get_articles(ARTICLES_ENDPOINT, articles);

    return { articles };
  },
};
</script>

<template>
  <div>
    {{ articles }}
  </div>
</template>

<style scoped>
</style>
