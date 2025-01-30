<template>
    <div>
        <embed :src="pdfUrl" type="application/pdf" width="100%" height="730px" />
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            pdfUrl: ''
        };
    },
    created() {
        const bookId = this.$route.params.bookId;
        this.fetchPdfUrl(bookId);
    },
    methods: {
        async fetchPdfUrl(bookId) {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/book/${bookId}`);
                this.pdfUrl = response.data.pdf_url;
            } catch (error) {
                console.error('Error fetching PDF URL:', error);
            }
        }
    }
};
</script>
  
<style scoped>

</style>
  