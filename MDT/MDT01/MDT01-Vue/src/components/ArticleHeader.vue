<script>
export default {
  props: {
    title: { type: String, required: true },
    abstract: { type: String, required: true },
    date: { type: String, required: true },
    modification: { type: String, required: true },
    duration: { type: Number, required: true },
  },
};
</script>

<template>
  <h1 class="title">{{ title }}</h1>
  <p>{{ abstract }}</p>

  <div id="meta">
    <div id="left">
      <span>Ecrit le {{ date }}</span>
      <span> / </span>
      <span>Dernière modification le {{ modification }}</span>
    </div>
    <div id="right">Temps de lecture: {{ duration }} {{ duration == 1 ? "minute" : "minutes" }}</div>
  </div>
</template>

<style scoped>
h1 {
    font-size: 40px;
    font-weight: 800;
}
p {
    font-size: 18px;
    font-weight: 600;
}
#meta {
    font-size: 0.9rem;
    display: flex;
    flex-direction: row;
    margin: 0 0 3rem 0;
}

#meta #left {
    display: flex;
    flex-direction: row;
    gap: 1rem;
}

#meta #right {
    align-self: right;
    margin-left: auto;
}
</style>
