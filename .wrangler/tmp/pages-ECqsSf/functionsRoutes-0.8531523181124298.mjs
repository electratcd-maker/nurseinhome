import { onRequestPost as __api_admin_login_js_onRequestPost } from "/data/data/com.termux/files/home/nurseinhome/functions/api/admin/login.js"
import { onRequestPost as __api_create_order_js_onRequestPost } from "/data/data/com.termux/files/home/nurseinhome/functions/api/create-order.js"
import { onRequestGet as __api_founder_js_onRequestGet } from "/data/data/com.termux/files/home/nurseinhome/functions/api/founder.js"
import { onRequest as __api___path___js_onRequest } from "/data/data/com.termux/files/home/nurseinhome/functions/api/[[path]].js"

export const routes = [
    {
      routePath: "/api/admin/login",
      mountPath: "/api/admin",
      method: "POST",
      middlewares: [],
      modules: [__api_admin_login_js_onRequestPost],
    },
  {
      routePath: "/api/create-order",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_create_order_js_onRequestPost],
    },
  {
      routePath: "/api/founder",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_founder_js_onRequestGet],
    },
  {
      routePath: "/api/:path*",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api___path___js_onRequest],
    },
  ]