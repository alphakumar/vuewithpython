<template>
  <div v-if="$route.name === 'home'" class="app-container">
    <header>
      <h1>Python (FastAPI) + Vue 3 App</h1>
      <p>Status Indicator:
        <span :class="statusClass">{{ backendStatus }}</span>
      </p>
    </header>
    <div>
      <!-- <router-link :to="{ name: 'CustomerForm' }">Add New Customer</router-link> -->
      <button @click="addNewCustomerForm" style="cursor:pointer">Add New Customer</button>
    </div>
    <table border="1" cellpadding="5" cellspacing="0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Contact</th>
          <th>Email</th>
          <th>Country</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in customers.data" :key="customer.CustomerId">
          <td>{{ customer.CustomerID }}</td>
          <td>{{ customer.CustomerName }}</td>
          <td>{{ customer.ContactNo }}</td>
          <td>{{ customer.Email }}</td>
          <td>{{ customer.Country }}</td>
          <td>
            <button @click="editCustomer(customer.CustomerID)" style="margin-right: 0.125rem;">Edit</button>
            <button @click="deleteCustomer(customer.CustomerID)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <router-view />
</template>

<script>
export default {
  data() {
    return {
      backendStatus: "Connecting...",
      isHealthy: false,
      customers: [],
    }
  },
  computed: {
    statusClass() {
      return this.isHealthy ? 'status-ok' : 'status-pending';
    }
  },
  mounted() {
    this.checkBackendHealth();
    this.fetchCustomers();
  },
  methods: {
    async checkBackendHealth() {
      // Pulls the backend URL dynamically from your .env.development file
      const baseUrl = import.meta.env.VITE_API_BASE_URL;

      try {
        const response = await fetch(`${baseUrl}/api/v1/health`);
        if (!response.ok) throw new Error("Server responded with an error");

        const data = await response.json();
        this.backendStatus = data.message;
        this.isHealthy = true;
      } catch (error) {
        this.backendStatus = "Disconnected from backend server.";
        this.isHealthy = false;
        console.error("CORS or Connection Error:", error);
      }
    },

    async fetchCustomers() {
      const baseUrl = import.meta.env.VITE_API_BASE_URL;

      try {
        const response = await fetch(`${baseUrl}/api/v1/get_customers`);
        console.log("response", response);
        if (!response.ok) throw new Error("Failed to fetch customers");

        const data = await response.json();
        console.log("Fetched customers:", data);
        this.customers = data;
      } catch (error) {
        console.error("Error fetching customers:", error);
      }
    },
    addNewCustomerForm() {
      console.log("open modal or form");
      // return this.$router.push({ name: 'CustomerForm' });
      this.$router.push('/CustomerForm')
    },

    editCustomer(customerId){
      console.log("Edit customer:", customerId);
      this.$router.push(`/CustomerForm/${customerId}`);
    },

    deleteCustomer(customerId) {
       console.log("Delete id", customerId);
       const baseurl = import.meta.env.VITE_API_BASE_URL;
       fetch(`${baseurl}/api/v1/delete_customer/${customerId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
       })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to delete customer');
        }
        // Remove the deleted customer from the list
        this.customers = this.customers.filter(customer => customer.CustomerID !== customerId);
      })
      .catch(error => {
        console.error("Error deleting customer:", error);
      });
    }

  }
}
</script>

<style scoped>
.app-container {
  font-family: Arial, sans-serif;
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}
.status-ok {
  color: #2ecc71;
  font-weight: bold;
}
.status-pending {
  color: #e74c3c;
  font-weight: bold;
}
</style>
