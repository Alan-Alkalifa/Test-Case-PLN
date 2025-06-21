<template>
  <div class="shadow-md rounded-lg mx-5 p-8 bg-white min-h-screen">
    <form @submit.prevent="handleSubmit" class="space-y-8">
      <!-- Informasi Ruang Meeting -->
      <div class="space-y-6">
        <h2 class="text-[16px] font-semibold text-[#333333]">Informasi Ruang Meeting</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="block text-[14px] font-semibold text-[#333333]">
              Unit <span class="text-red-500">*</span>
            </label>
            <select 
              v-model="form.unit" 
              class="w-full px-3 py-2 border border-[#D3D3D3] rounded-md text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#4A8394] focus:border-[#4A8394]"
              :class="{ 'border-red-500': errors.some(error => error.includes('Unit')) }"
              @change="loadMeetingRooms"
              required
            >
              <option value="">Pilih Unit</option>
              <option v-for="unit in masterUnits" :key="unit.id" :value="unit.id">
                {{ unit.officeName }}
              </option>
            </select>
          </div>
          
          <div class="space-y-2">
            <label class="block text-[14px] font-semibold text-[#333333]">
              Ruang Meeting <span class="text-red-500">*</span>
            </label>
            <select 
              v-model="form.ruangMeeting" 
              class="w-full px-3 py-2 border border-[#D3D3D3] rounded-md text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#4A8394] focus:border-[#4A8394]"
              :class="{ 'border-red-500': errors.some(error => error.includes('Ruang Meeting')) }"
              @change="updateCapacity"
              :disabled="!form.unit"
              required
            >
              <option value="">Pilih Ruang Meeting</option>
              <option v-for="room in meetingRooms" :key="room.id" :value="room.id">
                {{ room.roomName }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="space-y-2">
          <label class="block text-[14px] font-semibold text-[#333333]">Kapasitas</label>
          <input 
            type="number" 
            v-model="form.kapasitas" 
            class="w-full px-3 py-2 border border-[#D3D3D3] rounded-md bg-[#EEEEEE] text-[#333333]" 
            readonly
            :placeholder="form.kapasitas || '0'"
          />
        </div>
      </div>

      <!-- Divider -->
      <hr class="border-gray-200">

      <!-- Informasi Rapat -->
      <div class="space-y-6">
        <h2 class="text-[16px] font-semibold text-[#333333]">Informasi Rapat</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="space-y-2">
            <label class="block text-[14px] font-semibold text-[#333333]">
              Tanggal Rapat <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input 
                type="date" 
                v-model="form.tanggalRapat" 
                class="w-full px-3 py-2 border border-[#D3D3D3] rounded-md text-[#333333] focus:outline-none focus:ring-2 focus:ring-[#4A8394] focus:border-[#4A8394]"
                :class="{ 'border-red-500': errors.some(error => error.includes('Tanggal rapat')) }"
                required
              />
            </div>
          </div>
          
          <div class="space-y-2">
            <label class="block text-[14px] font-semibold text-[#333333]">
              Waktu Mulai <span class="text-red-500">*</span>
            </label>
            <select 
              v-model="form.waktuMulai" 
              class="w-full px-3 py-2 border border-[#D3D3D3] rounded-md text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#4A8394] focus:border-[#4A8394]"
              :class="{ 'border-red-500': errors.some(error => error.includes('Waktu mulai')) }"
              @change="calculateConsumption"
              required
            >
              <option value="">Pilih Waktu Mulai</option>
              <option v-for="time in timeSlots" :key="time" :value="time">{{ time }}</option>
            </select>
          </div>
          
          <div class="space-y-2">
            <label class="block text-[14px] font-semibold text-[#333333]">
              Waktu Selesai <span class="text-red-500">*</span>
            </label>
            <select 
              v-model="form.waktuSelesai" 
              class="w-full px-3 py-2 border border-[#D3D3D3] rounded-md text-gray-500 focus:outline-none focus:ring-2 focus:ring-[#4A8394] focus:border-[#4A8394]"
              :class="{ 'border-red-500': errors.some(error => error.includes('Waktu selesai')) }"
              @change="calculateConsumption"
              required
            >
              <option value="">Pilih Waktu Selesai</option>
              <option v-for="time in timeSlots" :key="time" :value="time">{{ time }}</option>
            </select>
          </div>
        </div>
        
        <div class="space-y-2">
          <label class="block text-[14px] font-semibold text-[#333333]">
            Jumlah Peserta <span class="text-red-500">*</span>
          </label>
          <input 
            type="number" 
            v-model="form.jumlahPeserta" 
            placeholder="Masukkan Jumlah Peserta"
            class="w-full px-3 py-2 border border-[#D3D3D3] rounded-md text-[#333333] focus:outline-none focus:ring-2 focus:ring-[#4A8394] focus:border-[#4A8394]"
            :class="{ 'border-red-500': errors.some(error => error.includes('Jumlah peserta')) }"
            @input="calculateConsumption"
            min="1"
            required
          />
        </div>
      </div>

      <!-- Jenis Konsumsi -->
      <div class="space-y-4">
        <h2 class="text-[16px] font-semibold text-[#333333]">Jenis Konsumsi</h2>
        <div class="space-y-3">
          <div v-if="masterJenisKonsumsi.length === 0" class="text-gray-500 text-[14px]">
            Loading konsumsi options...
          </div>
          <label v-for="konsumsi in masterJenisKonsumsi" :key="konsumsi.id" class="flex items-center space-x-3 cursor-pointer">
            <input 
              type="checkbox" 
              v-model="form.jenisKonsumsi" 
              :value="konsumsi.id"
              class="h-4 w-4 text-[#4A8394] focus:ring-[#4A8394] border-[#D3D3D3] rounded"
              @change="calculateConsumption"
            />
            <span class="text-[14px] text-[#333333]">{{ konsumsi.name }}</span>
          </label>
        </div>
      </div>

      <!-- Nominal Konsumsi -->
      <div class="space-y-2">
        <h2 class="text-[16px] font-semibold text-[#333333]">Nominal Konsumsi</h2>
        <div class="flex w-full">
          <span class="inline-flex items-center px-4 py-2 text-sm font-normal text-[#333333] bg-[#E5E7E9] rounded-l-lg border border-r-0 border-[#E5E7E9]">
            Rp.
          </span>
          <input
            type="text"
            :value="formatCurrency(form.nominalKonsumsi)"
            class="w-full px-4 py-2 border border-[#E5E7E9] rounded-r-lg bg-white text-[#333333] focus:outline-none"
            readonly
            :placeholder="form.nominalKonsumsi ? formatCurrency(form.nominalKonsumsi) : '0'"
          />
        </div>
      </div>

      <!-- Validation Errors -->
      <div v-if="errors.length > 0" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 class="text-red-800 font-semibold mb-2">Validasi Error:</h3>
        <ul class="text-red-700 text-[14px] space-y-1">
          <li v-for="error in errors" :key="error">• {{ error }}</li>
        </ul>
      </div>
      
      <!-- Divider -->
      <hr class="border-gray-200">
      
      <!-- Action Buttons -->
      <div class="flex justify-end space-x-3 pt-6">
        <button 
          type="button" 
          @click="resetForm"
          class="px-6 py-2 text-[#FF6363] hover:text-[#cd5a5a] focus:outline-none focus:ring-2 focus:ring-gray-500"
        >
          Batal
        </button>
        <button 
          type="submit"
          class="px-6 py-2 bg-[#D3D3D3] text-[#9E9E9E] rounded-md hover:bg-[#4A8394] hover:text-white focus:outline-none focus:ring-2 focus:ring-white"
        >
          Simpan
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FormRuangMeeting',
  data() {
    return {
      form: {
        unit: '',
        ruangMeeting: '',
        kapasitas: 0,
        tanggalRapat: '',
        waktuMulai: '',
        waktuSelesai: '',
        jumlahPeserta: '',
        jenisKonsumsi: [],
        nominalKonsumsi: 0
      },
      masterUnits: [],
      meetingRooms: [],
      masterJenisKonsumsi: [],
      timeSlots: [
        '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
        '16:00', '16:30', '17:00', '17:30', '18:00'
      ],
      errors: []
    }
  },
  async mounted() {
    await this.loadMasterData()
  },
  methods: {
    async loadMasterData() {
      try {
        // Load Master Units
        const unitsResponse = await axios.get('https://6666c7aea2f8516ff7a4e261.mockapi.io/api/dummy-data/masterOffice')
        this.masterUnits = unitsResponse.data

        // Load Master Jenis Konsumsi
        const konsumsiResponse = await axios.get('https://6686cb5583911b03a7f3.mockapi.io/api/dummy-data/masterJenisKonsumsi')
        this.masterJenisKonsumsi = konsumsiResponse.data
        
        console.log('Loaded consumption types:', this.masterJenisKonsumsi)
      } catch (error) {
        console.error('Error loading master data:', error)
        // Fallback data if API fails
        this.masterJenisKonsumsi = [
          {
            "createdAt": "2024-07-04T04:03:28.947Z",
            "name": "Snack Siang",
            "maxPrice": 20000,
            "id": "1"
          },
          {
            "createdAt": "2024-07-04T10:04:22.946Z",
            "name": "Makan Siang",
            "maxPrice": 30000,
            "id": "2"
          },
          {
            "createdAt": "2024-07-03T21:57:46.929Z",
            "name": "Snack Sore",
            "maxPrice": 20000,
            "id": "3"
          }
        ]
      }
    },
    
    async loadMeetingRooms() {
      if (!this.form.unit) {
        this.meetingRooms = []
        return
      }
      
      try {
        const response = await axios.get('https://6666c7aea2f8516ff7a4e261.mockapi.io/api/dummy-data/masterMeetingRooms')
        this.meetingRooms = response.data.filter(room => room.officeId === this.form.unit)
        
        // Reset ruang meeting selection when unit changes
        this.form.ruangMeeting = ''
        this.form.kapasitas = 0
      } catch (error) {
        console.error('Error loading meeting rooms:', error)
      }
    },
    
    updateCapacity() {
      const selectedRoom = this.meetingRooms.find(room => room.id === this.form.ruangMeeting)
      this.form.kapasitas = selectedRoom ? selectedRoom.capacity : 0
    },
    
    calculateConsumption() {
      // Reset consumption selection first
      this.form.jenisKonsumsi = []
      
      if (!this.form.waktuMulai || !this.form.waktuSelesai) {
        this.form.nominalKonsumsi = 0
        return
      }

      // Apply automatic consumption rules based on time
      this.applyConsumptionRules()
      
      // Calculate total nominal if participants are entered
      if (this.form.jumlahPeserta && this.form.jenisKonsumsi.length > 0) {
        let totalNominal = 0
        this.form.jenisKonsumsi.forEach(konsumsiId => {
          const konsumsi = this.masterJenisKonsumsi.find(k => k.id === konsumsiId)
          if (konsumsi) {
            totalNominal += konsumsi.maxPrice * parseInt(this.form.jumlahPeserta)
          }
        })
        this.form.nominalKonsumsi = totalNominal
      } else {
        this.form.nominalKonsumsi = 0
      }
      
      console.log('Calculated consumption:', {
        waktuMulai: this.form.waktuMulai,
        waktuSelesai: this.form.waktuSelesai,
        selectedKonsumsi: this.form.jenisKonsumsi,
        jumlahPeserta: this.form.jumlahPeserta,
        totalNominal: this.form.nominalKonsumsi
      })
    },
    
    applyConsumptionRules() {
      const startTime = this.form.waktuMulai
      const endTime = this.form.waktuSelesai
      
      // Convert time strings to minutes for easier comparison
      const startMinutes = this.timeToMinutes(startTime)
      const endMinutes = this.timeToMinutes(endTime)
      const time11 = this.timeToMinutes('11:00')
      const time14 = this.timeToMinutes('14:00')
      
      // Rule 1: Meeting mulai sebelum jam 11.00, mendapat snack siang
      if (startMinutes < time11) {
        const snackSiang = this.masterJenisKonsumsi.find(k => k.name === 'Snack Siang')
        if (snackSiang && !this.form.jenisKonsumsi.includes(snackSiang.id)) {
          this.form.jenisKonsumsi.push(snackSiang.id)
        }
      }
      
      // Rule 2: Meeting jam 11.00-14.00, mendapat makan siang
      if ((startMinutes >= time11 && startMinutes <= time14) || 
          (endMinutes >= time11 && endMinutes <= time14) ||
          (startMinutes < time11 && endMinutes > time14)) {
        const makanSiang = this.masterJenisKonsumsi.find(k => k.name === 'Makan Siang')
        if (makanSiang && !this.form.jenisKonsumsi.includes(makanSiang.id)) {
          this.form.jenisKonsumsi.push(makanSiang.id)
        }
      }
      
      // Rule 3: Meeting di atas jam 14.00, mendapat snack sore
      if (startMinutes > time14) {
        const snackSore = this.masterJenisKonsumsi.find(k => k.name === 'Snack Sore')
        if (snackSore && !this.form.jenisKonsumsi.includes(snackSore.id)) {
          this.form.jenisKonsumsi.push(snackSore.id)
        }
      }
    },
    
    timeToMinutes(timeString) {
      const [hours, minutes] = timeString.split(':').map(Number)
      return hours * 60 + minutes
    },
    
    validateForm() {
      this.errors = []
      
      // Unit validation
      if (!this.form.unit) {
        this.errors.push('Unit harus dipilih.')
      }
      
      // Meeting room validation
      if (!this.form.ruangMeeting) {
        this.errors.push('Ruang Meeting harus dipilih.')
      }
      
      // Date validation
      if (!this.form.tanggalRapat) {
        this.errors.push('Tanggal rapat harus diisi.')
      } else {
        // Check if date is not in the past
        const today = new Date().toISOString().split('T')[0]
        if (this.form.tanggalRapat < today) {
          this.errors.push('Tanggal rapat tidak boleh kurang dari tanggal hari ini.')
        }
      }
      
      // Start time validation
      if (!this.form.waktuMulai) {
        this.errors.push('Waktu mulai harus dipilih.')
      }
      
      // End time validation
      if (!this.form.waktuSelesai) {
        this.errors.push('Waktu selesai harus dipilih.')
      }
      
      // Time comparison validation
      if (this.form.waktuMulai && this.form.waktuSelesai) {
        if (this.form.waktuMulai >= this.form.waktuSelesai) {
          this.errors.push('Waktu mulai tidak boleh lebih besar atau sama dengan waktu selesai.')
        }
      }
      
      // Number of participants validation
      if (!this.form.jumlahPeserta) {
        this.errors.push('Jumlah peserta harus diisi.')
      } else {
        // Check if participants is a positive number
        if (parseInt(this.form.jumlahPeserta) <= 0) {
          this.errors.push('Jumlah peserta harus lebih dari 0.')
        }
        
        // Check capacity validation only if room is selected
        if (this.form.kapasitas && parseInt(this.form.jumlahPeserta) > this.form.kapasitas) {
          this.errors.push('Jumlah peserta tidak boleh lebih besar dari kapasitas ruangan.')
        }
      }
      
      return this.errors.length === 0
    },
    
    handleSubmit() {
      if (this.validateForm()) {
        // Submit the form
        console.log('Form submitted:', this.form)
        // Here you would typically send the data to your API
        alert('Form berhasil disimpan!')
      }
    },
    
    resetForm() {
      this.form = {
        unit: '',
        ruangMeeting: '',
        kapasitas: 0,
        tanggalRapat: '',
        waktuMulai: '',
        waktuSelesai: '',
        jumlahPeserta: '',
        jenisKonsumsi: [],
        nominalKonsumsi: 0
      }
      this.meetingRooms = []
      this.errors = []
    },
    
    formatCurrency(amount) {
      return new Intl.NumberFormat('id-ID').format(amount)
    }
  }
}
</script>

<style scoped>
/* Custom styles to match the design */
input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
}

select {
  appearance: none;
  background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 5"><path fill="%23666" d="M2 0L0 2h4zm0 5L0 3h4z"/></svg>');
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 12px;
  padding-right: 28px;
}

.form-group {
  margin-bottom: 1rem;
}

/* Error state styling */
.border-red-500 {
  border-color: #ef4444 !important;
}

/* Custom checkbox styling */
input[type="checkbox"]:checked {
  background-color: #4A8394 !important;
  border-color: #4A8394 !important;
}

input[type="checkbox"]:focus {
  box-shadow: 0 0 0 3px rgba(74, 131, 148, 0.1) !important;
}
</style>