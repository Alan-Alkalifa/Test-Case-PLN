<template>
    <div class="bg-[#F2F2F2] rounded-lg shadow-lg p-6 max-w-md mx-auto">
  
      <!-- Room Name -->
      <h3 class="text-[14px] font-normal text-[#4E4E4E]">{{ currentRoomData.roomName }}</h3>
  
      <!-- Usage Percentage -->
      <div class="mb-2">
        <div class="flex items-center justify-between mb-2">
          <div>
           <span class="text-[11px] text-[#625B71]">Persentase Pemakaian</span>
           <div class="text-[20px] font-bold text-[#000000]">{{ usagePercentage }}%</div>
          </div>
          <div class="w-15 h-15 relative">
            <!-- Circular Progress -->
            <svg class="w-15 h-15 transform -rotate-90" viewBox="0 0 36 36">
              <path
                class="text-gray-200"
                stroke="currentColor"
                stroke-width="4"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                class="text-[#00A3E9]"
                stroke="currentColor"
                stroke-width="4"
                fill="none"
                stroke-linecap="round"
                :stroke-dasharray="circleProgress"
                :stroke-dashoffset="circleOffset"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
          </div>
        </div>
      </div>
  
      <!-- Total Consumption -->
      <div class="mb-2">
        <span class="text-[11px] text-[#625B71]">Nominal Konsumsi</span>
        <div class="text-2xl font-bold text-[#000000] mt-1">
          Rp {{ formatNumber(totalConsumptionAmount) }}
        </div>
      </div>
  
      <!-- Consumption Items -->
      <div class="space-y-2">
        <div 
          v-for="item in consumptionItems" 
          :key="item.name"
          class="flex items-center justify-between"
        >
          <span class="text-black text-[10px] font-medium">{{ item.name }}</span>
          <div class="flex flex-col items-start">
            <span class="text-[20px] font-bold text-[#000000] mr-3">{{ item.totalPackage }}</span>
            <div class="w-14 h-2 bg-gray-200 rounded-full">
              <div 
                class="h-2 bg-[#00A3E9] rounded-full"
                :style="{ width: getBarWidth(item.totalPackage) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CardDashboard',
    props: {
      unitTitle: {
        type: String,
        default: 'UNIT INDUK 1'
      },
      apiUrl: {
        type: String,
        required: false
      },
      roomData: {
        type: Object,
        default: () => ({})
      },
      isMockData: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        internalRoomData: {},
        consumptionItems: [],
        loading: true,
        error: null
      }
    },
    computed: {
      currentRoomData() {
        return this.isMockData ? this.roomData : this.internalRoomData;
      },
      usagePercentage() {
        if (!this.currentRoomData.capacity || !this.currentRoomData.averageOccupancyPerMonth) {
          return 0;
        }
        const percentage = (parseInt(this.currentRoomData.averageOccupancyPerMonth) / parseInt(this.currentRoomData.capacity)) * 100;
        return Math.round(percentage * 100) / 100;
      },
      circleProgress() {
        const circumference = 2 * Math.PI * 15.9155;
        return `${circumference} ${circumference}`;
      },
      circleOffset() {
        const circumference = 2 * Math.PI * 15.9155;
        const progress = this.usagePercentage / 100;
        return circumference - (progress * circumference);
      },
      totalConsumptionAmount() {
        return this.consumptionItems.reduce((total, item) => {
          return total + parseInt(item.totalPrice || 0);
        }, 0);
      },
      maxPackages() {
        if (this.consumptionItems.length === 0) return 1;
        return Math.max(...this.consumptionItems.map(item => parseInt(item.totalPackage || 0)));
      }
    },
    methods: {
      async fetchData() {
        if (this.isMockData) {
          // Use mock data directly
          this.consumptionItems = this.roomData.totalConsumption || [];
          this.loading = false;
          return;
        }
  
        if (!this.apiUrl) {
          this.loading = false;
          return;
        }
  
        try {
          this.loading = true;
          const response = await fetch(this.apiUrl);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const apiData = await response.json();
          
          // Process the API data structure
          if (apiData.data && apiData.data.length > 0) {
            const officeData = apiData.data[0]; // Get first office
            if (officeData.detailSummary && officeData.detailSummary.length > 0) {
              const firstRoom = officeData.detailSummary[0]; // Get first room
              this.internalRoomData = {
                roomName: firstRoom.roomName || 'Nama Ruangan 1',
                capacity: firstRoom.capacity || '0',
                averageOccupancyPerMonth: firstRoom.averageOccupancyPerMonth || '0'
              };
              this.consumptionItems = firstRoom.totalConsumption || [];
            }
          }
        } catch (error) {
          console.error('Error fetching data:', error);
          this.error = error.message;
          // Set default data in case of error
          this.internalRoomData = {
            roomName: 'Nama Ruangan 1',
            capacity: '75',
            averageOccupancyPerMonth: '65'
          };
          this.consumptionItems = [
            { name: 'Snack Siang', totalPackage: '140', totalPrice: '2800000' },
            { name: 'Makan Siang Siang', totalPackage: '280', totalPrice: '8400000' },
            { name: 'Snack Sore', totalPackage: '140', totalPrice: '2800000' }
          ];
        } finally {
          this.loading = false;
        }
      },
      formatNumber(number) {
        return new Intl.NumberFormat('id-ID').format(number);
      },
      getBarWidth(packages) {
        const value = parseInt(packages || 0);
        return (value / this.maxPackages) * 100;
      }
    },
    mounted() {
      this.fetchData();
    },
    watch: {
      roomData: {
        handler() {
          if (this.isMockData) {
            this.consumptionItems = this.roomData.totalConsumption || [];
          }
        },
        immediate: true,
        deep: true
      }
    }
  }
  </script>
  
  <style scoped>
  /* Additional custom styles if needed */
  .shadow-lg {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  </style>