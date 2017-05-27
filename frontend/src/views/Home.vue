<template>

<el-row class="tac">
  <el-row class="container">
    <!--<el-col :span="4">-->
      <!--<h5>带 icon</h5>-->
      <!--<el-menu default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">-->
        <!--<el-submenu index="1">-->
          <!--<template slot="title"><i class="el-icon-message"></i>导航一</template>-->
          <!--<el-menu-item-group>-->
            <!--<template slot="title">分组一</template>-->
            <!--<el-menu-item index="1-1">选项1</el-menu-item>-->
            <!--<el-menu-item index="1-2">选项2</el-menu-item>-->
          <!--</el-menu-item-group>-->
          <!--<el-menu-item-group title="分组2">-->
            <!--<el-menu-item index="1-3">选项3</el-menu-item>-->
          <!--</el-menu-item-group>-->
          <!--<el-submenu index="1-4">-->
            <!--<template slot="title">选项4</template>-->
            <!--<el-menu-item index="1-4-1">选项1</el-menu-item>-->
          <!--</el-submenu>-->
        <!--</el-submenu>-->
        <!--<el-menu-item index="2"><i class="el-icon-menu"></i>导航二</el-menu-item>-->
        <!--<el-menu-item index="3"><i class="el-icon-setting"></i>导航三</el-menu-item>-->
      <!--</el-menu>-->
    <!--</el-col>-->
    <!--<el-col :span="20">-->

    <!--</el-col>-->
    <el-col :span="24" class="header">
    </el-col>
    <el-col :span="24" class="main">
    </el-col>
  </el-row>
</el-row>

</template>

<script>
  export default {
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<style scoped>

  .container {
    position: absolute;
    top: 0px;
    bottom: 0px;
    height: 500px;
    width: 100%;
  }
  .header {
    height: 60px;
    line-height: 60px;
    color:#fff;
  }
  .main {
  / / background: #324057;
    position: absolute;
    top: 60px;
    bottom: 0px;
    overflow: hidden;
  }

</style>
