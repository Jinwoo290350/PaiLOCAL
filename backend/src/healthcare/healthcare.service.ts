import { Injectable } from '@nestjs/common';

@Injectable()
export class HealthcareService {
  checkHealth() {
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'healthcare',
      message: 'Healthcare service is up and running'
    };
  }
}
