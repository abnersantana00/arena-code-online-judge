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
    };


  },


  created() {
    this.setDarkMode();
  },
  methods: {
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
    onSubmit() {
      console.log('submit!', this.form);
      ElMessage({
        message: 'Form submitted successfully!',
        type: 'success',
      });

    },
    handleRowClick(row) {
      // Redireciona para a página do tópico com base no topic_id
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
