<script setup lang="ts">
import { ref, onMounted } from 'vue';
import CardDashboard from '../card/CardDashboard.vue';

// Reactive data
const units = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedPeriod = ref('January 2024');

// API endpoint
const API_URL = 'https://6686cb5583c983911b03a7f3.mockapi.io/api/dummy-data/summaryBookings';

// Fetch data from API
const fetchDashboardData = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const apiData = await response.json();
    console.log('API Response:', apiData);
    
    // Process the API data
    if (Array.isArray(apiData) && apiData.length > 0) {
      // Take the first item from the array
      const firstItem = apiData[0];
      
      if (firstItem.data && Array.isArray(firstItem.data)) {
        // Create units from the data
        units.value = firstItem.data.map((office, index) => {
          const unitNumber = index + 1;
          return {
            title: `UNIT INDUK ${unitNumber}`,
            officeName: office.officeName || `Office ${unitNumber}`,
            rooms: office.detailSummary || []
          };
        });
        
        // If we need exactly 5 units, we can duplicate or create additional ones
        while (units.value.length < 5) {
          const existingUnit = units.value[units.value.length % firstItem.data.length];
          const newUnitNumber = units.value.length + 1;
          units.value.push({
            title: `UNIT INDUK ${newUnitNumber}`,
            officeName: existingUnit.officeName,
            rooms: existingUnit.rooms
          });
        }
      }
    }
    
    // Fallback if no data or unexpected structure
    if (units.value.length === 0) {
      console.warn('No valid data found, using fallback structure');
      // Create default structure
      const defaultRoom = {
        roomName: "Nama Ruangan 1",
        capacity: "75",
        averageOccupancyPerMonth: "65",
        totalConsumption: [
          { name: "Snack Siang", totalPackage: "140", totalPrice: "2800000" },
          { name: "Makan Siang Siang", totalPackage: "280", totalPrice: "8400000" },
          { name: "Snack Sore", totalPackage: "140", totalPrice: "2800000" }
        ]
      };
      
      units.value = Array.from({ length: 5 }, (_, i) => ({
        title: `UNIT INDUK ${i + 1}`,
        officeName: `Office ${i + 1}`,
        rooms: Array.from({ length: 3 }, (_, j) => ({
          ...defaultRoom,
          roomName: `Nama Ruangan ${j + 1}`
        }))
      }));
    }
    
  } catch (err) {
    console.error('Error fetching dashboard data:', err);
    error.value = err.message;
    
    // Fallback data in case of error
    const defaultRoom = {
      roomName: "Nama Ruangan 1",
      capacity: "75",
      averageOccupancyPerMonth: "65",
      totalConsumption: [
        { name: "Snack Siang", totalPackage: "140", totalPrice: "2800000" },
        { name: "Makan Siang Siang", totalPackage: "280", totalPrice: "8400000" },
        { name: "Snack Sore", totalPackage: "140", totalPrice: "2800000" }
      ]
    };
    
    units.value = Array.from({ length: 5 }, (_, i) => ({
      title: `UNIT INDUK ${i + 1}`,
      officeName: `Office ${i + 1}`,
      rooms: Array.from({ length: 3 }, (_, j) => ({
        ...defaultRoom,
        roomName: `Nama Ruangan ${j + 1}`
      }))
    }));
  } finally {
    loading.value = false;
  }
};

// Fetch data on component mount
onMounted(() => {
  fetchDashboardData();
});
</script>

<template>
  <div class="w-full flex flex-col min-h-screen bg-gray-50 p-6 ">
    <!-- Header -->
    <div class="bg-white rounded-t-lg shadow-sm p-6">
      <div class="flex items-center justify-between">
        <nav class="flex items-center gap-4">
          <div class="w-6 h-6 text-gray-600">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
            </svg>
          </div>
          <h1 class="text-xl font-bold text-gray-800">DASHBOARD</h1>
        </nav>
        <div class="text-gray-400">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
          </svg>
        </div>
      </div>
      
      <!-- Divider -->
      <div class="border-b border-gray-200 my-6"></div>
      
      <!-- Period Selector -->
      <div class="flex flex-col gap-2">
        <label class="text-xs font-medium text-gray-600 uppercase tracking-wide">
          Periode
        </label>
        <select 
          v-model="selectedPeriod"
          @change="fetchDashboardData"
          class="border border-gray-300 rounded-md px-3 py-2 max-w-xs text-[12px] font-medium bg-white text-black focus:outline-none focus:ring-2 focus:ring-[#00A3E9] focus:border-[#00A3E9]"
        >
          <option value="January 2024">Januari 2024</option>
          <option value="February 2024">Februari 2024</option>
          <option value="March 2024">Maret 2024</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#00A3E9]"></div>
      <span class="ml-3 text-gray-600">Loading dashboard data...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
      <div class="flex items-center">
        <div class="w-5 h-5 text-red-500 mr-3">
          <svg fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
        </div>
        <div>
          <h3 class="text-sm font-medium text-red-800">Error loading data</h3>
          <p class="text-sm text-red-600 mt-1">{{ error }}</p>
        </div>
      </div>
      <button 
        @click="fetchDashboardData" 
        class="mt-4 bg-red-600 text-white px-4 py-2 rounded-md text-sm hover:bg-red-700 transition-colors"
      >
        Retry
      </button>
    </div>
<!-- Cards Grid -->
<div v-else class="bg-white rounded-b-lg shadow-sm py-6">
  <!-- Units as columns -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6 px-6">
    <!-- Each unit as a column -->
    <div v-for="(unit, unitIndex) in units" :key="unitIndex" class="space-y-4">
      <!-- Unit Title -->
      <h3 class="text-[16px] font-semibold text-[#868E96] text-center flex gap-4"><img src="/src/components/icons/IconLighting.svg" alt="Iocn Lighting" class="w-[18] h-[23]">{{ unit.title }}</h3>
      
      <!-- Rooms stacked vertically in this unit column -->
      <div class="space-y-4">
        <div v-for="(room, roomIndex) in unit.rooms" :key="`${unitIndex}-${roomIndex}`">
          <CardDashboard 
            :unit-title="unit.title"
            :room-data="room"
            :is-mock-data="true"
          />
        </div>
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<style scoped>
/* Custom scrollbar if needed */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>