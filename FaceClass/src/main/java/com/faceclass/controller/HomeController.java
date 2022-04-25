package com.faceclass.controller;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.google.gson.Gson;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import com.faceclass.common.DateUtil;
import com.faceclass.entity.User;
import com.faceclass.service.UserService;

import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

@Controller  
@RequestMapping(value = "")  
public class HomeController {  
	@Resource(name = "userService")  
    UserService userService;  

	//改
	@RequestMapping(value = "/index")
	public String index(){
		return "index";
	}
	@RequestMapping(value = "/facelogin")
    public String facelogin(HttpServletRequest request, HttpServletResponse response, Model model){

	try{
		String base = request.getParameter("base");
//		System.out.println(base);
		String name_id = getResult(base);
		System.out.println(name_id);
		PrintWriter writer = response.getWriter();
		response.reset();
		if(name_id.equals("Stranger")){
			request.setAttribute("errMsg","您还为注册账号，请先注册账号");
			return null;
		}
		User user = userService.getUser(name_id);
		if( user.getUserStatus() == 1 ){//等于1，表示用户状态可用，否则“禁用”
			request.getSession().setAttribute("user",user);
			writer.print(name_id);
			writer.close();
			return null;
		}else{
			request.setAttribute("errMsg","此账号已被禁用！！");
			return null;
		}

	}catch (Exception e){
		e.printStackTrace();

	}

	return null;
    }

	public String getResult(String imStr1){
		System.out.println("imStr1:"+imStr1);
		boolean flag = false;
		BufferedReader br = null;
		String result = "";
		String name = "";
		String Url = "http://127.0.0.1:5000/face";
		try{
			String params = URLEncoder.encode("images", "UTF-8") + "="

					+ URLEncoder.encode(imStr1, "UTF-8");
			URL url = new URL(Url);
			HttpURLConnection connection = (HttpURLConnection) url
					.openConnection();
			connection.setRequestMethod("POST");
			connection.setRequestProperty("Content-Type",
					"application/x-www-form-urlencoded");
			connection.setRequestProperty("Connection", "Keep-Alive");
			connection.setDoInput(true);
			connection.setDoOutput(true);

			DataOutputStream out = new DataOutputStream(
					connection.getOutputStream());
			out.writeBytes(params);
			out.flush();
			out.close();
			br = new BufferedReader(new InputStreamReader(
					connection.getInputStream()));
			String line = "";
			while ((line = br.readLine()) != null) {
				result += line;
			}
			br.close();
		}catch (Exception e){
			e.printStackTrace();
		}
//		System.out.println(result);
		Gson gson = new Gson();
		Map<String, String> map = new HashMap<String, String>();
		map = gson.fromJson(result, map.getClass());
		String name_id=map.get("name");
		System.out.println(name_id);
		return name_id;

	}

	/**
	 * 眨眼检测
	 */
	@RequestMapping(value = "/faceeyecheck")
	public  String faceeyecheck(HttpServletRequest request,HttpServletResponse response){

		try{

			String base = request.getParameter("base");
			Double eye = getEye(base);
			PrintWriter writer = response.getWriter();
			response.reset();
			writer.print(eye);
			writer.close();
			return null;
		}catch (Exception e){
			e.printStackTrace();
		}
		return null;
	}

	public Double getEye(String imStr1){
		//System.out.println("imStr1:"+imStr1);
		boolean flag = false;
		BufferedReader br = null;
		String result = "";
		String name = "";
		String Url = "http://127.0.0.1:5000/faceeyecheck";
		try{
			String params = URLEncoder.encode("images", "UTF-8") + "="

					+ URLEncoder.encode(imStr1, "UTF-8");
			URL url = new URL(Url);
			HttpURLConnection connection = (HttpURLConnection) url
					.openConnection();
			connection.setRequestMethod("POST");
			connection.setRequestProperty("Content-Type",
					"application/x-www-form-urlencoded");
			connection.setRequestProperty("Connection", "Keep-Alive");
			connection.setDoInput(true);
			connection.setDoOutput(true);

			DataOutputStream out = new DataOutputStream(
					connection.getOutputStream());
			out.writeBytes(params);
			out.flush();
			out.close();
			br = new BufferedReader(new InputStreamReader(
					connection.getInputStream()));
			String line = "";
			while ((line = br.readLine()) != null) {
				result += line;
			}
			br.close();
		}catch (Exception e){
			e.printStackTrace();
		}
//		System.out.println(result);
		Gson gson = new Gson();
		Map<String, Double> map = new HashMap<String, Double>();
		map = gson.fromJson(result, map.getClass());
		Double EAR=map.get("ear");
		System.out.println(EAR);
		return EAR;

	}

    /**
	 * 	登录页面
	 */
    @RequestMapping(value = "/login")  
    public String login(HttpSession session){
    	User user = new User();
    	user = (User) session.getAttribute("user");
    	if( user != null ){
    		return "redirect:/me";
    	}
        return "login";
    }
    
    /**
	 * 	用户登录验证成功-->我的页面
	 */
    @RequestMapping(value = "/loginCheck",method=RequestMethod.POST)  
    public String loginCheck(String account, String password, HttpServletRequest request){
    	//System.out.println("用户登录---输入的账号和姓名："+account+","+password);
    	User user = userService.getUser(account);
    	if( user != null ){	//如果不等于空说明账号正确
    		if( user.getUserPassword().equals(password) ){
    			if( user.getUserStatus() == 1 ){//等于1，表示用户状态可用，否则“禁用”
    				request.getSession().setAttribute("user",user);
    				return "redirect:/me";
    			}else{
    				request.setAttribute("errMsg","此账号已被禁用！！");
    				return "login";
    			}
			}else{
				request.setAttribute("errMsg","密码错误！！");
				return "login";
			}
    	}else{
    		request.setAttribute("errMsg","账号不存在！！");//账号不存在！
			return "login";
		}
    }
    
    /**
   	 * 	到达-->注册页面
   	 */
    @RequestMapping(value = "/register",method=RequestMethod.GET)  
    public String register(){
    	return "register";
    }
    
    /**
   	 * 	注册页面
   	 */
    @RequestMapping(value = "/registerCheck",method=RequestMethod.POST)  
    public String register(String account, String password, HttpServletRequest request){
    	System.out.println("用户注册---输入的账号和姓名："+account+","+password);
    	User user = new User();
    	user.setUserId(account);
    	user.setUserPassword(password);
    	user.setUserPhoto("anonymous-photo.png");	//设置默认头像
    	user.setUserStatus(1);						//设置默认状态可用
    	DateUtil dateUtil = new DateUtil();
    	//设置注册时间
    	user.setUserRegisterTime(dateUtil.getCurrentTime());
    	int result = userService.addUserSelective(user);
    	if( result == 1 ){	//注册成功
    		System.out.println("用户注册成功");
    		request.setAttribute("message", "注册成功");
    		return "register";
    	}else{	// 注册失败
    		System.out.println("用户注册失败");
    		request.setAttribute("message", "注册失败");
    		return "register";
    	}
    }
    
    /**
   	 * 	退出-->登录页面
   	 */
    @RequestMapping(value = "/layout",method=RequestMethod.GET)  
    public String layout(HttpSession session,HttpServletRequest request){
    	System.out.println("用户退出成功");
    	session.removeAttribute("user");
    	session.invalidate();
    	// System.out.println("用户退出---"+session.getAttribute("user"));
    	return "login";
    }

    
}  