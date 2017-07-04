<template>
  <el-row class="home" >
    <oms-head></oms-head>
    <el-row style="height: 100%">
      <el-col :span="4" style="height: 100%">
        <side-bar></side-bar>
      </el-col>
      <el-col :span="20" style="padding: 15px;height: 100%">
        <project-list></project-list>
      </el-col>
    </el-row>
  </el-row>

</template>

<script>
  import ProjectList from '../components/ProjectList.vue'
  import OmsHead from '../components/OmsHead.vue'
  import SideBar from '../components/SideBar.vue'
  export default {
    components: {
      ProjectList,
      OmsHead,
      SideBar
    },
  }

</script>

<style scoped>
  .home {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
  }






</style>
