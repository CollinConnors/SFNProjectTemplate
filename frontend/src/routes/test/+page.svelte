
<script>
  import axios from 'axios';
  import { onMount } from 'svelte';
  import {backend_api} from "../../stores/servers"
  
  let endpoint = backend_api+'/';
  /**
	 * @type {String}
	 */
  let get_res = "false";

  /**
	 * @type {String}
	 */
  let post_res = "false";

  onMount(async () => {
    const response = await axios.get(endpoint);
    if (response.data.hasOwnProperty("alive")) {
      get_res = response.data.alive;
    }
  });

  async function postAlive() {
    const data = {alive:"true"};
    const response = await axios({method:'POST',url:endpoint,data:data});
    if (response.data.hasOwnProperty("alive")) {
      post_res = response.data.alive;
    }
  }


</script>

<h3 class="font-medium leading-tight text-3xl mt-0 mb-2 text-blue-600"> Test Page</h3>

<p class="p-1">GET Alive: {get_res}</p>


  <button
    type="button"
    data-mdb-ripple="true"
    data-mdb-ripple-color="light"
    class="inline-block px-2 py-2.5 bg-grey-200 rounded shadow-md" on:click={postAlive}>Send Post</button>

<p>POST Alive: {post_res}</p>