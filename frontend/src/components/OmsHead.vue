<template>
  <el-row class="header" type="flex" justify="end">
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
</template>

<script>
  export default {
      data(){
        return {
          sysName: "OMS",
          sysUserName: "chens"
        }
      }
  }
</script>

<style scoped>
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
