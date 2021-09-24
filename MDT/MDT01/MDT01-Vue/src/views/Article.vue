<script>
import ArticleContent from "../components/ArticleContent.vue";
import ArticleHeader from "../components/ArticleHeader.vue";

export default {
  components:{
    "ArticleHeader": ArticleHeader,
    "ArticleContent": ArticleContent
  },
  props: {
    title: { type: String, required: true },
    abstract: { type: String, required: true },
    date: { type: String, required: true },
    modification: { type: String, required: true },
    duration: { type: Number, required: true },
    content: { type: String, required: true }
  }
}
</script>

<template>
  <ArticleHeader
    :title="title"
    :abstract="abstract"
    :date="date"
    :modification="modification"
    :duration=duration
  />

  <ArticleContent :content="content"/>
</template>

<style>
</style>
