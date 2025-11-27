import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js';
import { EstimationAccuracy } from '../../../../core/models/analytics.model';

@Component({
  selector: 'app-estimation-chart',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './estimation-chart.component.html',
  styleUrls: ['./estimation-chart.component.scss']
})
export class EstimationChartComponent implements OnInit, OnChanges {
  @Input() data!: EstimationAccuracy;
  @Input() showTrend = true;
  @Input() fullWidth = false;

  // Line Chart for Trend
  lineChartData: ChartData<'line'> = {
    labels: [],
    datasets: []
  };

  lineChartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom'
      },
      tooltip: {
        backgroundColor: '#172B4D',
        padding: 12,
        cornerRadius: 8
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        min: 50,
        max: 100,
        ticks: {
          callback: (value) => value + '%'
        },
        grid: {
          color: '#EBECF0'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    },
    elements: {
      line: {
        tension: 0.4
      },
      point: {
        radius: 4,
        hoverRadius: 6
      }
    }
  };

  // Doughnut Chart for Distribution
  doughnutChartData: ChartData<'doughnut'> = {
    labels: ['Accurate', 'Over-estimated', 'Under-estimated'],
    datasets: []
  };

  doughnutChartOptions: ChartConfiguration<'doughnut'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom'
      }
    },
    cutout: '70%'
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

    // Update Line Chart
    this.lineChartData = {
      labels: this.data.monthlyTrend.map(t => t.month),
      datasets: [
        {
          label: 'Acceptance Rate',
          data: this.data.monthlyTrend.map(t => t.acceptanceRate),
          borderColor: '#0052CC',
          backgroundColor: 'rgba(0, 82, 204, 0.1)',
          fill: true
        }
      ]
    };

    // Update Doughnut Chart
    this.doughnutChartData = {
      labels: ['Accurate', 'Over-estimated', 'Under-estimated'],
      datasets: [
        {
          data: [
            this.data.accurateEstimations,
            this.data.overEstimations,
            this.data.underEstimations
          ],
          backgroundColor: ['#36B37E', '#FFAB00', '#FF5630'],
          borderWidth: 0
        }
      ]
    };
  }
}