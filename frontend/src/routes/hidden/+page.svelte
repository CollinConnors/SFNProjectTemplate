
<script>
	import { redirect } from '@sveltejs/kit';
    import axios from 'axios';
    import { onMount } from 'svelte';
    import {backend_api, fronend_server_dev, fronend_server_prod, dev} from "../../stores/servers";
    
    let endpoint = backend_api+'/hidden';
    
    let fronend_server = "";

    if (dev){
        fronend_server = fronend_server_dev;
    }
    else{
        fronend_server = fronend_server_prod;
    }
    
    /**
       * @type {String}
       */
    let get_res = "You are not logged in!";
  
    /**
       * @type {String}
       */
    let post_res = "false";

    /**
	 * @param {string} cookiename
	 */
    function getCookie(cookiename) {
    // Get name followed by anything except a semicolon
    var cookiestring=RegExp(cookiename+"=[^;]+").exec(document.cookie);
    // Return everything after the equal sign, or an empty string if the cookie name not found
    return decodeURIComponent(!!cookiestring ? cookiestring.toString().replace(/^[^=]+./,"") : "");
    }
    

  
    onMount(async () => {
    
        try{
            const response = await axios.get(endpoint, { headers: {Authorization: 'Bearer '+getCookie('jwt')} });
            if (response.data.hasOwnProperty("alive")) {
                get_res = response.data.alive;
            }
        }
        catch{
            window.location.replace(fronend_server+"/login");
        }

    });
  
    async function postAlive() {
        try{
            const data = {alive:"true"};
            const header = {Authorization: 'Bearer '+getCookie('jwt')}
            const response = await axios({method:'POST',url:endpoint, data:data, headers:header});
            if (response.data.hasOwnProperty("alive")) {
                post_res = response.data.alive;
            }
        }
        catch{
            window.location.replace(fronend_server+"/login");
        }
    }
  
  
  </script>
  
  <h3 class="font-medium leading-tight text-3xl mt-0 mb-2 text-blue-600"> Hidden Test Page</h3>
  
  <p class="p-1">GET Alive: {get_res}</p>
  
  
    <button
      type="button"
      data-mdb-ripple="true"
      data-mdb-ripple-color="light"
      class="inline-block px-2 py-2.5 bg-grey-200 rounded shadow-md" on:click={postAlive}>Send Post</button>
  
  <p>POST Alive: {post_res}</p>