const { createApp } = Vue;
const {
  ElContainer, ElHeader, ElMain, ElFooter, ElButton, ElRow, ElCol, ElTable,
  ElTableColumn, ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElMessage,
  ElAvatar, ElTag, ElCard, ElDivider, ElImage, ElText, ElLink, ElSpace, ElBreadcrumbItem,
  ElBreadcrumb,
} = ElementPlus;



const app = createApp({
  delimiters: ['[[', ']]'],  // Alterando os delimitadores para evitar conflitos com Django

  data() {
    return {
      isDarkMode: true,
      form : {
        code :'',
      }
    };

  },


  created() {
    this.setDarkMode();
  },
  methods: {

    onSubmit() {
      const formData = new FormData();
      formData.append('code', this.form.code);

      // Construa a URL dinâmica usando os parâmetros
      const url = `/${this.topic}/${this.title_name}/source-code/`;

      fetch(url, {
        method: 'POST',
        body: formData
      })
      .then(response => response.text())
      .then(data => {
        console.log('Success:', data);
        // Redireciona para a página do tópico
        window.location.href = `source-code`;
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },

    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      this.setDarkMode();
    },

    setDarkMode() {
      if (this.isDarkMode) {
        document.documentElement.setAttribute('class', 'dark');
      } else {
        document.documentElement.removeAttribute('class', 'dark');
      }
    },

    handleRowClick(row) {
      // Redireciona para a página do tópico com base no topic_id
      window.location.href = `/topic/${row.topic_id}`;
      const url = `${row.topic_name}`;
      window.location.href = url;
    },


  }
});


app.component('el-container', ElContainer);
app.component('el-header', ElHeader);
app.component('el-main', ElMain);
app.component('el-footer', ElFooter);
app.component('el-button', ElButton);
app.component('el-row', ElRow);
app.component('el-col', ElCol);
app.component('el-table', ElTable);
app.component('el-table-column', ElTableColumn);
app.component('el-form', ElForm);
app.component('el-form-item', ElFormItem);
app.component('el-input', ElInput);
app.component('el-select', ElSelect);
app.component('el-option', ElOption);
app.component('el-avatar', ElAvatar);
app.component('el-tag', ElTag);
app.component('el-card', ElCard);
app.component('el-divider', ElDivider);
app.component('el-image', ElImage);
app.component('el-text', ElText);
app.component('el-link', ElLink);
app.component('el-space', ElSpace);
app.component('el-breadcrumb-item', ElBreadcrumbItem);
app.component('el-breadcrumb', ElBreadcrumb);



app.mount('#app');




