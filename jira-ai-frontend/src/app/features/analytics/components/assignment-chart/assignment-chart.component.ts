import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData } from 'chart.js';
import { AssignmentAccuracy } from '../../../../core/models/analytics.model';

@Component({
  selector: 'app-assignment-chart',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './assignment-chart.component.html',
  styleUrls: ['./assignment-chart.component.scss']
})
export class AssignmentChartComponent implements OnInit, OnChanges {
  @Input() data!: AssignmentAccuracy;

  barChartData: ChartData<'bar'> = {
    labels: [],
    datasets: []
  };

  barChartOptions: ChartConfiguration<'bar'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: '#EBECF0'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    }
  };

  pieChartData: ChartData<'pie'> = {
    labels: ['Auto-assigned', 'Manual Override', 'Reassigned'],
    datasets: []
  };

  pieChartOptions: ChartConfiguration<'pie'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom'
      }
    }
  };

  ngOnInit(): void {
    this.updateCharts();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['data']) {
      this.updateCharts();
    }
  }

  private updateCharts(): void {
    if (!this.data) return;

    // Bar chart - assignments by member
    const topMembers = this.data.assignmentsByMember.slice(0, 5);
    this.barChartData = {
      labels: topMembers.map(m => m.displayName.split(' ')[0]),
      datasets: [
        {
          label: 'Completed',
          data: topMembers.map(m => m.completed),
          backgroundColor: '#36B37E'
        },
        {
          label: 'Reassigned',
          data: topMembers.map(m => m.reassigned),
          backgroundColor: '#FFAB00'
        }
      ]
    };

    // Pie chart - assignment distribution
    const autoOnly = this.data.autoAssigned - this.data.reassignments;
    this.pieChartData = {
      labels: ['Auto-assigned', 'Manual Override', 'Reassigned'],
      datasets: [
        {
          data: [autoOnly, this.data.manualOverrides, this.data.reassignments],
          backgroundColor: ['#0052CC', '#6554C0', '#FFAB00'],
          borderWidth: 0
        }
      ]
    };
  }

  getAcceptanceClass(): string {
    if (this.data.acceptanceRate >= 80) return 'high';
    if (this.data.acceptanceRate >= 60) return 'medium';
    return 'low';
  }
}