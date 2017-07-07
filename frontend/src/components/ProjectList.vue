<template>
  <div>
    <el-row :span="1">
      <el-col :span="20">
        <strong class="title" style="margin-bottom: 10px">Docker Stack:</strong>
      </el-col>
      <el-col :span="4" align="right">
        <el-button type="primary" @click="handleProjectAdd" style="margin-bottom: 10px" icon="plus">新增</el-button>
        <el-button type="info" style="margin-bottom: 10px" @click="getProjects">刷新</el-button>
      </el-col>
    </el-row>
    <el-row :span="23" font-family="Helvetica Neue">
      <section>
        <!--project tree-->
        <el-tree
          :data="projectTree"
          :props="defaultProps"
          v-loading="delProjectLoading"
          element-loading-text="拼命加载中"
          element-loading-fullscreen
          node-key="id"
          :expand-on-click-node="false"
          :render-content="renderContent"
          >
        </el-tree>

        <!--工具条-->
        <!--<el-col :span="24" class="toolbar">-->
          <!--<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>-->
          <!--<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">-->
          <!--</el-pagination>-->
        <!--</el-col>-->

        <!--编辑界面-->
        <el-dialog title="编辑" v-model="editProjectFormVisible" :close-on-click-modal="false">
          <el-form :model="editProjectForm" label-width="80px" ref="editProjectForm">
            <el-form-item label="项目" prop="name">
              <el-input v-model="editProjectForm.name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="yaml">
              <el-input type="textarea" v-model="editProjectForm.yaml" :autosize="{ minRows: 2, maxRows: 20 }"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="editProjectFormVisible = false">取消</el-button>
            <el-button type="primary" @click.native="editProjectSubmit" :loading="editProjectSubmitLoading">修改</el-button>
          </div>
        </el-dialog>

        <!--服务扩容-->
        <!--<el-dialog title="服务扩容" v-model="serviceScaleVisible" :close-on-click-modal="false">-->
        <!--</el-dialog>-->
        <el-dialog
          title="服务扩容"
          :visible.sync="serviceScaleVisible"
          size="tiny"
          :model="currentService"
          >
          <el-form label-width="80px" ref="serviceScaleForm">
            <el-form-item label="服务:">
              {{currentService.label}}
            </el-form-item>
            <el-form-item label="当前实例:">
              {{currentService.replicas.current}}
            </el-form-item>
            <el-form-item label="配置实例:">
              {{currentService.replicas.total}}
            </el-form-item>
            <el-form-item label="扩容:">
              <el-input-number v-model="serviceReplicas" :step="1" :min="1"></el-input-number>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="serviceScaleVisible = false">取消</el-button>
            <el-button type="primary" @click="putServiceScale">提交</el-button>
          </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" v-model="newProjectFormVisible" :close-on-click-modal="false">
          <el-form :model="newProjectForm" label-width="80px" :rules="newProjectFormRules" ref="newProjectForm">
            <el-form-item label="项目" prop="name">
              <el-input v-model="newProjectForm.name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="yaml">
              <el-input type="textarea" v-model="newProjectForm.content" :autosize="{ minRows: 2, maxRows: 20 }"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="newProjectFormVisible = false">取消</el-button>
            <el-button type="primary" @click.native="newProjectSubmit" :loading="newProjectSubmitLoading">创建</el-button>
            <el-button type="primary" :loading="newProjectSubmitLoading">创建并部署</el-button>
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
    created(){
      this.getProjects()
    },
    data() {
      return {
        filters: {
          name: ''
        },
        currentService: {
            replicas: {}
        },
        serviceReplicas: 1,
        projectTree: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        total: 0,
        page: 1,
        listLoading: false,
        sels: [],//列表选中列

        delProjectLoading: false, //删除加载
        editProjectFormVisible: false,//编辑界面是否显示
        editProjectSubmitLoading: false,
        //编辑界面数据
        editProjectForm: {},

        serviceScaleVisible: false, //
        newProjectFormVisible: false,//新增界面是否显示
        newProjectSubmitLoading: false,
        newProjectFormRules: {
          name: [
            { required: true, message: '请输入项目名', trigger: 'blur' }
          ]
        },
        //新增界面数据
        newProjectForm: {
          name: '',
          content: ''
        }

      }
    },
    methods: {
      append(store, data) {
        store.append({ id: id++, label: 'testtest', children: [] }, data);
      },

      remove(store, data) {
        store.remove(data);
      },
      renderContent:function(createElement, { node, data, store }) {
        let that = this;
        let attrs = data.state === 'deployed'? { type: "success"}: {};
        if(data.isProjectNode){
          return createElement('span', [
            createElement('span', node.label),
            createElement('span', {attrs:{
                style:"float: right; margin-right: 20px"
                }},[
                    createElement('el-tag',
                      {
                        attrs: attrs
                      }, data.state
                    ),
                    createElement('el-button',{attrs:{
                        size:"small",
                        icon: "edit"
                    },on:{
                        click:function() {
                          console.log("点击了" + data.label + "的编辑按钮");
                          that.handleProjectEdit(data.label);
                        },
                    }},"编辑"),
                    createElement('el-button',
                      {
                        attrs: {
                          size: "small",
                          type: "primary",
                          icon: "caret-right",
                          loading: data.deployLoading,
//                          disabled: startButtonDisabled
                        },
                        on: {
                            click: function () {
                              that.deployProject(data);
                            }
                        },
                      }, "部署"
                    ),
                    createElement('el-button',{attrs:{
                        size: "small",
                        type: "danger",
                        icon: "delete2"
                    },on:{
                        click:function() {
                          console.log("点击了" + data.label + "的删除按钮");
                          that.handleDel(data.label);
                        }
                    }},"删除"),
                ]),
          ]);
        }
        else {
          let that = this;
          let state = data.uuid? "running": "stopped";
          let stateType = data.uuid? "success": "gray";
          let replicas = data.replicas? data.replicas: { current: "-", total: "-"};
          let startButtonDisabled = data.uuid? true: false;
          return createElement('span', [
            createElement('span',
              {
                attrs: {

                },
              },
              [
                createElement('i',
                  {
                    attrs:{
                      class: "el-icon-star-on",
                      style: "margin-right: 5px"
                    }
                  },
                ),
                createElement('span', node.label),
              ]
            ),
            createElement('span', {
                attrs: {
                  style:"float: right; margin-right: 20px"
                }
              }, [
                createElement('el-tag',
                  {
                    attrs:{
                      type: stateType
                    }
                  }, state
                ),
                createElement('el-tag',
                  {
                    attrs:{
                      type:"primary"
                    }
                  }, replicas.current + "/" + replicas.total + "实例"
                ),
                createElement('el-button-group',
                  {
                    attrs: {
                      style:"margin-left: 20px"
                    },
                  },
                  [
                    createElement('el-button',
                      {
                        attrs: {
                          size: "small",
                          type: "primary",
                          icon: "plus",
                          disabled: !startButtonDisabled
                        },
                        on: {
                            click: function () {
                              that.serviceReplicas = data.replicas.total;
                              that.handleServiceScale(data)
                            }
                        },
                      }, "扩容"
                    ),
                    createElement('el-button',
                      {
                        attrs: {
                          size: "small",
                          type: "danger",
                          icon: "delete",
                          disabled: !startButtonDisabled
                        },
                        on: {
                            click: function () {
                              that.delService(data);
                            }
                        },
                      }, "删除"
                    ),
                  ]
                ),
            ])
          ])
        }

      },
      getProjects(){
        let that = this;
        let params = {
          url:"/projects",
        };
        api.get(params)
          .then(function(res){
            console.log(res.data.body.items);
            that.projectTree = [];
            res.data.body.items.forEach((item, i) => {
                let children = [];
                item.services.forEach((service, j) => {
                    children[j] = {
                        id: j,
                        label: service.displayName,
                        isProjectNode: false,
                        uuid: service.uuid,
                        replicas: service.replicas,
                        image: service.image,
                        serviceName: service.serviceName,
                        mode: service.mode,
                        project: item.name
                    }
                });
                that.projectTree[i] = {
                    id: i,
                    state: item.state,
                    label: item.name,
                    deployLoading: false,
                    isProjectNode: true,
                    children: children
                }
            });
          })
          .catch(function(err){
            console.log(err);
            api.reqFail(that,"获取列表失败请刷新");
          });
        console.log("projectTree: ");
        console.log(this.projectTree);
      },
      getProject(projectName){
        let that = this;
        let params = {
          url:"/projects/" + projectName + "/yml",
        };
        api.get(params)
          .then(function(res){
            console.log("get " + projectName);
            console.log(res.data.body);
            that.editProjectForm = Object.assign(res.data.body, {name: projectName})
          })
          .catch(function(err){
            console.log(err);
            api.reqFail(that,"获取项目失败请刷新");
          });
      },
      deleteProject(projectName){
        let that = this;
        that.delProjectLoading = true;
        let params = {
          url:"/projects/" + projectName + "/yml",
        };
        api.delete(params)
          .then(function(res){
            that.delProjectLoading = false
            console.log("delete " + projectName);
            console.log(res.data.body);
            that.$message({
              message: '删除成功',
              type: 'success'
            });
            that.getProjects()
          })
          .catch(function(err){
            that.delProjectLoading = false
            console.log(err);
            api.reqFail(that,"删除项目失败！");
          });
      },
      postProject(data) {
        let that = this;
        let param = {
            url: "/projects",
            data: data
        };
        api.post(param)
          .then(function(res){
            console.log("post project:");
            console.log(res.data);
            //NProgress.done();
            if(res.data.code === 1){
              that.$message({
                message: res.data.message,
                type: 'error'
              })
            }
            else{
              that.$message({
                message: '提交成功',
                type: 'success'
              });
              that.newProjectFormVisible = false;
              that.getProjects()
            }
          })
          .catch(function(err){
            console.log(err);
            api.reqFail(that,"创建项目失败");
          });
      },
      deployProject(project) {
        let that = this;
        project.deployLoading = true;
        console.log("deployProjectLoading");
        console.log(project);
        let param = {
            url: "/projects/" + project.label ,
        };
        api.post(param)
          .then(function(res){
            project.deployLoading = false;
            console.log("deploy project:");
            console.log(res.data);
            //NProgress.done();
            if(res.data.code === 1){
              that.$message({
                message: res.data.message,
                type: 'error'
              })
            }
            else{
              that.$message({
                message: '部署成功',
                type: 'success'
              });
              that.getProjects()
            }
          })
          .catch(function(err){
            project.deployLoading = false;
            console.log(err);
            api.reqFail(that,"部署项目失败");
          });
      },
      putProject(projectName, yaml_str) {
        let that = this;
        let param = {
            url:"/projects/" + projectName + "/yml",
            data: {
                yaml: yaml_str
            }
        };
        api.put(param)
          .then(function(res){
            console.log("put project:");
            console.log(res.data);
            //NProgress.done();
            if(res.data.code === 1){
              that.$message({
                message: res.data.message,
                type: 'error'
              })
            }
            else{
              that.$message({
                message: '修改成功',
                type: 'success'
              });
              that.getProjects();
              that.editProjectFormVisible = false
            }
          })
          .catch(function(err){
            console.log(err);
            api.reqFail(that,"post project失败");
          });
      },
      //性别显示转换
      formatSex: function (row, column) {
        return row.sex == 1 ? '男' : row.sex == 0 ? '女' : '未知';
      },
      handleCurrentChange(val) {
        this.page = val;
        this.getUsers();
      },
      putServiceScale(){
        let that = this;
        let param = {
            url:"/projects/" + that.currentService.project + "/services/" + that.currentService.serviceName + "/scale",
            data: {
                replicas: that.serviceReplicas
            }
        };
        console.log(param)
        api.put(param)
          .then(function(res){
            if(res.data.code === 1){
              that.$message({
                message: res.data.message,
                type: 'error'
              })
            }
            else{
              that.$message({
                message: '扩容成功',
                type: 'success'
              });
              that.getProjects();
              that.serviceScaleVisible = false
            }
          })
          .catch(function(err){
            console.log(err);
            api.reqFail(that,"put scale");
          });
      },
      delService(service){
        let that = this;
        let param = {
            url:"/projects/" + service.project + "/services/" + service.serviceName + "/remove",
        };
        console.log(param)
        api.delete(param)
          .then(function(res){
            if(res.data.code === 1){
              that.$message({
                message: res.data.message,
                type: 'error'
              })
            }
            else{
              that.$message({
                message: '删除成功',
                type: 'success'
              });
              that.getProjects();
            }
          })
          .catch(function(err){
            console.log(err);
            api.reqFail(that,"delete service");
          });
      },
      //删除
      handleDel: function (projectName) {
        this.$confirm('确认删除该记录吗?', '提示', {
          type: 'warning'
        }).then(() => {
          this.deleteProject(projectName);
        }).catch(() => {

        });
      },
      //显示编辑界面
      handleProjectEdit: function (projectName) {
        this.getProject(projectName)
        this.editProjectFormVisible = true;
//        this.editForm = Object.assign({}, row);
      },
      //显示新增界面
      handleProjectAdd: function () {
        this.newProjectFormVisible = true;
      },
      handleServiceScale: function (service) {
        this.currentService = service;
        this.serviceScaleVisible = true;
      },
      //编辑
      editProjectSubmit: function () {
        this.$refs.editProjectForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              console.log('editProjectForm:');
              console.log(this.editProjectForm);
              this.editProjectSubmitLoading = true;
              this.putProject(this.editProjectForm.name, this.editProjectForm.yaml)
              this.editProjectSubmitLoading = false;
            });
          }
        });
      },
      //新增
      newProjectSubmit: function () {
        this.$refs.newProjectForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.newProjectSubmitLoading = true;
              this.postProject(this.newProjectForm)
              this.newProjectSubmitLoading = false;
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
//      this.getUsers();
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
