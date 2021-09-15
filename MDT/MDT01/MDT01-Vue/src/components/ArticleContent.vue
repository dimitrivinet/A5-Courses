<script>
export default {
  props: {
    content: { type: String, required: true }
  }
};
</script>

<template>
  <p id="content" v-html="content"></p>
</template>

<style scoped>
#content {
    text-align: justify;
}

#content p {
    background-color: red;
}

figure {
    display: flex;
    flex-direction: column;
}
</style>
