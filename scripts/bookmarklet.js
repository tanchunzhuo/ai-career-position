// ============================================================
// bookmarklet.js — 网页 JD 提取书签
// 《AI职业选位》反爬合规方案：不自动登录、不批量爬取、不存 cookie。
// 用户在当前招聘页（BOSS直聘/猎聘/通用网页）**主动点击书签**，
// 脚本把当前页可见的 JD 文本 POST 到本地 http://localhost:8787/inbox。
//
// 安装方法（一次性）：
//   1. 先启动本地服务：python3 scripts/inbox_server.py
//   2. 浏览器新建书签，名称随意（如"存JD"），网址粘贴下面编译后的 javascript: 代码
//   3. 打开任意 JD 页面，点该书签 → 页面跳转到"已收入 Inbox"
//
// 生成编译版：复制本文件核心函数，用任意 bookmarklet 生成器压缩为一行，
//   或以 node 运行本仓库 docs 提供的 encode 脚本（见注释底部）。
// ============================================================

(function () {
  "use strict";
  var endpoint = "http://localhost:8787/inbox";

  // ---- 选择器适配：BOSS直聘 / 猎聘 / 通用 ----
  var titleSelectors = [
    // BOSS直聘：职位名
    '.name', '.job-name', '[class*="job-name"] h1', 'h1',
    // 猎聘：职位名
    '.job-title', 'h1[class*="job"]',
    // 通用：h1 或 title
    'title'
  ];
  var companySelectors = [
    '.company-name', '.name-text', '[class*="company"] .name',
    '.job-company h3', '.company',
    'meta[property="og:site_name"]'
  ];
  var salarySelectors = [
    '.salary', '.salary-text', '.job-salary', '[class*="salary"]',
    '.job-info .salary'
  ];
  var contentSelectors = [
    '.job-sec-text', '.job-detail', '.job-description', '[class*="job-detail"]',
    '.text', '.content', 'article', 'body'
  ];

  function q1(list) {
    for (var i = 0; i < list.length; i++) {
      var el = document.querySelector(list[i]);
      if (el && el.textContent.trim()) return el;
    }
    return null;
  }

  var titleEl = q1(titleSelectors);
  var title = titleEl ? titleEl.textContent.trim().split('\n')[0].slice(0, 120) : document.title;
  var companyEl = q1(companySelectors);
  var company = companyEl ? companyEl.textContent.trim().slice(0, 60) : "";
  var salaryEl = q1(salarySelectors);
  var salary = salaryEl ? salaryEl.textContent.trim().slice(0, 80) : "";

  // 正文：优先正文容器，其次 body 全文（截断 20000 字符）
  var contentEl = q1(contentSelectors);
  var content = "";
  if (contentEl) {
    // 排除 script/style/nav/header/footer 噪音
    var clone = contentEl.cloneNode(true);
    clone.querySelectorAll('script,style,nav,header,footer,button,.sidebar,[class*="footer"]').forEach(function (n) {
      n.remove();
    });
    content = clone.innerText || clone.textContent || "";
  }
  content = content.replace(/\s+/g, "\n").trim().slice(0, 20000);

  var payload = {
    title: title,
    company: company,
    salary: salary,
    url: window.location.href,
    source: window.location.hostname,
    captured_at: new Date().toISOString(),
    content: content
  };

  // POST 到本地服务
  fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  }).then(function (r) {
    if (r.ok) window.location.href = endpoint;
    else alert("保存失败，请确认本地服务已启动（python3 scripts/inbox_server.py）");
  }).catch(function () {
    alert("无法连接本地服务。请先运行：python3 scripts/inbox_server.py，并允许浏览器访问 http://localhost:8787");
  });
})();

// ------------------------------------------------------------
// 生成"一行书签"的方法（任选其一）：
// 1) 用任意 bookmarklet 压缩工具：把上方 IIFE 压缩成一行，前缀 javascript:
// 2) 或用 node 生成：
//    node -e "
//    const fs=require('fs');
//    let s=fs.readFileSync('scripts/bookmarklet.js','utf8');
//    s=s.split('// ---------')[0].replace(/\/\/[^\n]*\n/g,'').replace(/\s+/g,' ').trim();
//    console.log('javascript:'+encodeURIComponent(s));"
//    然后把输出粘贴为书签网址。
// 注意：部分浏览器对书签 URL 长度有限制，若超限请精简 contentSelectors。
// ------------------------------------------------------------
