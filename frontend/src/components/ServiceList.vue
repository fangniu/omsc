<template>
  <div>
    <el-row :span="1">

      <strong class="title" style="margin-bottom: 15px">服务栈:</strong>

    </el-row>
    <el-row :span="23" font-family="Helvetica Neue">
      <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
          <el-form :inline="true" :model="filters">
            <el-form-item>
              <el-input v-model="filters.name" placeholder="栈名"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" v-on:click="getUsers">查询</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleAdd">新增</el-button>
            </el-form-item>
          </el-form>
        </el-col>

        <!--列表-->
        <el-table :data="stack_list" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <el-table-column prop="name" label="服务栈" span="4" sortable>
          </el-table-column>
          <el-table-column prop="services" label="服务" span="14" sortable type="expand">
          </el-table-column>
          <el-table-column label="操作" span="6">
            <template scope="scope">
              <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
          <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
          <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
          </el-pagination>
        </el-col>

        <!--编辑界面-->
        <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
          <el-form :model="editForm" label-width="80px" ref="editForm">
            <el-form-item label="服务栈" prop="name">
              <el-input v-model="editForm.name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="ID号" prop="id">
              <el-input v-model="editForm.id"></el-input>
            </el-form-item>
            <el-form-item label="yaml">
              <el-input type="textarea" v-model="editForm.yml" :autosize=true></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="editFormVisible = false">取消</el-button>
            <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
          </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
          <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
            <el-form-item label="栈名" prop="name">
              <el-input v-model="addForm.name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="性别">
              <el-radio-group v-model="addForm.sex">
                <el-radio class="radio" :label="1">男</el-radio>
                <el-radio class="radio" :label="0">女</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="年龄">
              <el-input-number v-model="addForm.age" :min="0" :max="200"></el-input-number>
            </el-form-item>
            <el-form-item label="生日">
              <el-date-picker type="date" placeholder="选择日期" v-model="addForm.birth"></el-date-picker>
            </el-form-item>
            <el-form-item label="地址">
              <el-input type="textarea" v-model="addForm.addr"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="addFormVisible = false">取消</el-button>
            <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
          </div>
        </el-dialog>
      </section>
    </el-row>
  </div>


</template>

<script>
  import API from '../api/API'
  const api = new API();
  export default {
    beforeMount(){
      let that = this;
      let params = {
        url:"/kmxes",
      };
      api.get(params)
        .then(function(res){
          console.log(JSON.parse(res.data.data).sets[0].rows);
        })
        .catch(function(err){
          console.log('11');
          api.reqFail(that,"获取列表失败请刷新");
        });
    },
    data() {
      return {
        filters: {
          name: ''
        },
        stack_list: [  {
          name: 'myWeb',
          services: "web, redis, db"
        }],
        total: 0,
        page: 1,
        listLoading: false,
        sels: [],//列表选中列

        editFormVisible: false,//编辑界面是否显示
        editLoading: false,
        //编辑界面数据
        editForm: {
          id: 0,
          name: 'myWeb',
          yml: "version: \"3\"\nservices:\n\n  redis:\n    image: redis:alpine\n    ports:\n      - \"6379\"\n    networks:\n      - frontend\n    deploy:\n      replicas: 2\n      update_config:\n        parallelism: 2\n        delay: 10s\n      restart_policy:\n        condition: on-failure\n  db:\n    image: postgres:9.4\n    volumes:\n      - db-data:/var/lib/postgresql/data\n    networks:\n      - backend\n    deploy:\n      placement:\n        constraints: [node.role == manager]\n  vote:\n    image: dockersamples/examplevotingapp_vote:before\n    ports:\n      - 5000:80\n    networks:\n      - frontend\n    depends_on:\n      - redis\n    deploy:\n      replicas: 2\n      update_config:\n        parallelism: 2\n      restart_policy:\n        condition: on-failure\n  result:\n    image: dockersamples/examplevotingapp_result:before\n    ports:\n      - 5001:80\n    networks:\n      - backend\n    depends_on:\n      - db\n    deploy:\n      replicas: 1\n      update_config:\n        parallelism: 2\n        delay: 10s\n      restart_policy:\n        condition: on-failure\n\n  worker:\n    image: dockersamples/examplevotingapp_worker\n    networks:\n      - frontend\n      - backend\n    deploy:\n      mode: replicated\n      replicas: 1\n      labels: [APP=VOTING]\n      restart_policy:\n        condition: on-failure\n        delay: 10s\n        max_attempts: 3\n        window: 120s\n      placement:\n        constraints: [node.role == manager]\n\n  visualizer:\n    image: manomarks/visualizer\n    ports:\n      - \"8080:8080\"\n    stop_grace_period: 1m30s\n    volumes:\n      - \"/var/run/docker.sock:/var/run/docker.sock\"\n    deploy:\n      placement:\n        constraints: [node.role == manager]\n\nnetworks:\n  frontend:\n  backend:\n\nvolumes:\n  db-data:\n"
        },

        addFormVisible: false,//新增界面是否显示
        addLoading: false,
        addFormRules: {
          name: [
            { required: true, message: '请输入姓名', trigger: 'blur' }
          ]
        },
        //新增界面数据
        addForm: {
          name: '',
          sex: -1,
          age: 0,
          birth: '',
          addr: ''
        }

      }
    },
    methods: {
      //性别显示转换
      formatSex: function (row, column) {
        return row.sex == 1 ? '男' : row.sex == 0 ? '女' : '未知';
      },
      handleCurrentChange(val) {
        this.page = val;
        this.getUsers();
      },
      //获取用户列表
      getUsers() {
        let para = {
          page: this.page,
          name: this.filters.name
        };
        this.listLoading = true;
        //NProgress.start();
//        getUserListPage(para).then((res) => {
//          this.total = res.data.total;
//          this.users = res.data.users;
//          this.listLoading = false;
//          //NProgress.done();
//        });
        this.total = 1
        this.users = [  {
          id: 1,
          username: 'admin',
          password: '123456',
          avatar: 'https://raw.githubusercontent.com/taylorchen709/markdown-images/master/vueadmin/user.png',
          name: '张某某'
        }]
        this.listLoading = false;

      },
      //删除
      handleDel: function (index, row) {
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          //NProgress.start();
          let para = { id: row.id };
          removeUser(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.getUsers();
          });
        }).catch(() => {

        });
      },
      //显示编辑界面
      handleEdit: function (index, row) {
        this.editFormVisible = true;
        console.log(this.editForm)
//        this.editForm = Object.assign({}, row);
      },
      //显示新增界面
      handleAdd: function () {
        this.addFormVisible = true;
        this.addForm = {
          name: '',
          sex: -1,
          age: 0,
          birth: '',
          addr: ''
        };
      },
      //编辑
      editSubmit: function () {
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              //NProgress.start();
              let para = Object.assign({}, this.editForm);
              para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
              editUser(para).then((res) => {
                this.editLoading = false;
                //NProgress.done();
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['editForm'].resetFields();
                this.editFormVisible = false;
                this.getUsers();
              });
            });
          }
        });
      },
      //新增
      addSubmit: function () {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.addLoading = true;
              //NProgress.start();
              let para = Object.assign({}, this.addForm);
              para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
              addUser(para).then((res) => {
                this.addLoading = false;
                //NProgress.done();
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['addForm'].resetFields();
                this.addFormVisible = false;
                this.getUsers();
              });
            });
          }
        });
      },
      selsChange: function (sels) {
        this.sels = sels;
      },
      //批量删除
      batchRemove: function () {
        var ids = this.sels.map(item => item.id).toString();
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          //NProgress.start();
          let para = { ids: ids };
          batchRemoveUser(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.getUsers();
          });
        }).catch(() => {

        });
      }
    },
    mounted() {
      this.getUsers();
    }
  }

</script>

<style scoped>
  .title {
    width: 200px;
    float: left;
    color: #475669;
  }
</style>
