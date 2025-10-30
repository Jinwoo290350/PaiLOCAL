import { Controller, Get, Version } from '@nestjs/common';
import { HealthcareService } from './healthcare.service';

@Controller('healthcare')
export class HealthcareController {
  constructor(private readonly healthcareService: HealthcareService) {}
    
  @Get('health')
  checkHealth() {
    return this.healthcareService.checkHealth();
  }
}
