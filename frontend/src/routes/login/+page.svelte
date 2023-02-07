<script>
    import axios from 'axios';
    import {backend_api, fronend_server_dev, fronend_server_prod, dev} from "../../stores/servers";
    import cookie from 'cookie';
    
    let fronend_server = "";
    if (dev){
        fronend_server = fronend_server_dev;
    }
    else{
        fronend_server = fronend_server_prod;
    }

    // @ts-ignore
    async function submitForm(e) {
        const formData = new FormData(e.target);
        let endpoint = backend_api+'/login';
        const data = {};
        for (let field of formData) {
            const [key, value] = field;
            // @ts-ignore
            data[key] = value;
        }
        console.log(data);
        const response = await axios({method:'POST',url:endpoint,data:data});
        if (response.data.hasOwnProperty("jwt")) {
            const jwt = response.data.jwt;
            console.log(jwt);
            document.cookie = cookie.serialize('jwt', jwt, {
                path: '/',
                sameSite: 'strict',
                secure: true,
                maxAge: 60 * 60 * 24
            });
            window.location.replace(fronend_server+"/hidden");
        }
    }
  
  
  </script>
  
  <!-- Example form from https://tailwind-elements.com/docs/standard/components/login-form/#! -->
  <section class="h-screen">
    <div class="px-6 h-full text-gray-800">
      <div
        class="flex xl:justify-center lg:justify-between justify-center items-center flex-wrap h-full g-6"
      >
        <div
          class="grow-0 shrink-1 md:shrink-0 basis-auto xl:w-6/12 lg:w-6/12 md:w-9/12 mb-12 md:mb-0"
        >
          <!-- svelte-ignore a11y-img-redundant-alt -->
          <img
            src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
            class="w-full"
            alt="Sample image"
          />
        </div>
        <div class="xl:ml-20 xl:w-5/12 lg:w-5/12 md:w-8/12 mb-12 md:mb-0">
          <form on:submit|preventDefault={submitForm}>
            <!-- Email input -->
            <div class="mb-6">
              <input
                type="text"
                class="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                placeholder="Username"
                name = "username"
                value = ""
              />
            </div>
  
            <!-- Password input -->
            <div class="mb-6">
              <input
                type="password"
                class="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                placeholder="Password"
                name = "password"
                value = ""
              />
            </div>
            
            <!-- Submit Button -->
            <div class="text-center lg:text-left">
              <button
                type="submit"
                class="inline-block px-7 py-3 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
              >
                Login
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>
  </section>