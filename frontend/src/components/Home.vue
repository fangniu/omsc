<template>
  <el-row class="container" >
    <el-row class="header"  type="flex" justify="end">
      <el-col :span="4" class="logo">{{sysName}}</el-col>
      <el-col :span="20" class="userinfo">
        <el-dropdown trigger="hover">
          <span class="el-dropdown-link userinfo-inner">{{ sysUserName}}<img src="../assets/logo.png" /></span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>我的消息</el-dropdown-item>
            <el-dropdown-item>设置</el-dropdown-item>
            <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-col>
    </el-row>
    <el-row class="main">
      <el-col class="navigation" :span="4">
        <el-menu default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-message"></i>导航一</template>
            <el-menu-item-group>
              <template slot="title">分组一</template>
              <el-menu-item index="1-1">选项1</el-menu-item>
              <el-menu-item index="1-2">选项2</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="分组2">
              <el-menu-item index="1-3">选项3</el-menu-item>
            </el-menu-item-group>
            <el-submenu index="1-4">
              <template slot="title">选项4</template>
              <el-menu-item index="1-4-1">选项1</el-menu-item>
            </el-submenu>
          </el-submenu>
          <el-menu-item index="2"><i class="el-icon-menu"></i>导航二</el-menu-item>
          <el-menu-item index="3"><i class="el-icon-setting"></i>导航三</el-menu-item>
        </el-menu>
      </el-col>
      <el-col>aaaa</el-col>
    </el-row>
  </el-row>

</template>

<script>
  export default {
    data() {
      return {
        sysName:'OMS',
        collapsed:false,
        sysUserName: 'chens',
        sysUserAvatar: '../assets/logo.png',
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        }
      }
    },
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
    top: 0;
    bottom: 0;
    width: 100%;
  }
  .header {
    height: 60px;
    line-height: 60px;
    background: #20a0ff;
    color: #fff;
  }
  .logo {
    height:60px;
    font-size: 22px;
    padding-left:20px;
    padding-right:20px;
    border-color: rgba(238, 241, 146, 0.3);
    border-right: 1px solid;
  }
  .main {
    /*display: flex;*/
    height: 100%;
    /*position: absolute;*/
    /*top: 60px;*/
    /*bottom: 0;*/
    /*overflow: hidden;*/
  }
  .navigation {
    left: 0;
    padding-left: 0;
    background: #eef1f6;
    height: 100%;
  }
  .userinfo {
    text-align: right;
    padding-right: 35px;
    float: right;
  }
  .userinfo-inner {
    cursor: pointer;
    color: #fff;
  }
  .userinfo img {
    width: 40px;
    height: 40px;
    border-radius: 20px;
    margin: 10px 0 10px 10px;
    float: right;
  }



</style>
