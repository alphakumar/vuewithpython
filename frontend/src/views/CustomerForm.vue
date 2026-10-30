<template>
  <div >
    <h1>Customer Form</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="customerName">Customer Name:</label>
        <input type="text" id="customerName" v-model="customer.CustomerName" required />
      </div>
      <div>
        <label for="contactNo">Contact No:</label>
        <input type="text" id="contactNo" v-model="customer.ContactNo" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="customer.Email" required />
      </div>
      <div>
        <label for="country">Country:</label>
        <input type="text" id="country" v-model="customer.Country" required />
      </div>
      <button type="submit" >Submit</button>
      <router-link to="/" style="margin-left: 10px;">
        <button>Back</button>
      </router-link>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customer: {
        CustomerName: '',
        ContactNo: '',
        Email: '',
        Country: ''
      },
      customerId: null
    }
  },

  mounted() {
    this.getCustomerIdFromRoute();
    console.log('mounted custid', this.customerId);
    if (this.customerId) {
      this.fetchCustomer(this.customerId);
    }
  },
  computed: {
    // editButtonText() {
    //   return this.customerId ? 'Update' : 'Add Customer';
    // }
  },

  methods: {
    async submitForm() {
      const baseUrl = import.meta.env.VITE_API_BASE_URL;

      try {
        // const response = await fetch(`${baseUrl}/api/v1/create_customer`, {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json'
        //   },
        //   body: JSON.stringify(this.customer)
        // });
        // console.log('response data', response);
        let response;
        if(this.customerId > 0){
          const customerId = this.customerId;
          console.log('customerIdinsidesub', customerId);
          console.log('send url', (`${baseUrl}/api/v1/update_customer/${customerId}`));
           response = await fetch(`${baseUrl}/api/v1/update_customer/${customerId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.customer)
          });
          console.log('response data', response);

        }else{
           response = await fetch(`${baseUrl}/api/v1/create_customer`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.customer)
          });
          console.log('response data', response);
        }

        if (!response.ok) throw new Error("Failed to add customer");

        const data = await response.json();
        console.log("Customer added:", data);
        // Reset the form or navigate back to the customer list
        this.customer = { CustomerName: '', ContactNo: '', Email: '', Country: '' };
      } catch (error) {
        console.error("Error adding customer:", error);
      }
    },

    getCustomerIdFromRoute() {
      console.log("getcustomerid", this.$route.params.customerId);
      this.customerId = this.$route.params.customerId || null;
      console.log("this.customerId", this.customerId);
    },

    async fetchCustomer(customerId) {
      console.log('fetchcustid', customerId);
      const baseUrl = import.meta.env.VITE_API_BASE_URL;

      try {
        console.log('fetchcustidinside', customerId);
        console.log('baseUrl', baseUrl);
        const response = await fetch(`${baseUrl}/api/v1/get_customer/${customerId}`);
        // const response = await fetch(`${baseUrl}/api/v1/get_customers`);
        console.log('responsedata', response);
        if (!response.ok) throw new Error("Failed to fetch customer data");

        const data = await response.json();
        this.customer = data.data;
      } catch (error) {
        console.error("Error fetching customer:", error);
      }
    }

  }
}
</script>


